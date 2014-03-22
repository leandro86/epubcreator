import zipfile
import os

from lxml import etree

from epubcreator.converters import converter_base, xml_utils
from epubcreator import ebook_data
from epubcreator.converters.docx import utils, styles, footnotes


class DocxConverter(converter_base.AbstractConverter):
    _MAX_HEADING_NUMBER = 6

    _DOCUMENT_CONTENT_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"
    _STYLES_CONTENT_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"
    _FOOTNOTES_CONTENT_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml"

    # De haber imágenes, deben estar en este directorio dentro del docx.
    _MEDIA_FILES_PATH = "word/media"

    def __init__(self, inputFile, ignoreEmptyParagraphs=True):
        super().__init__(inputFile)

        self._documentXml = None
        self._documentRelsXml = None
        self._styles = None
        self._footnotes = None
        self._mediaFiles = {}

        self._ignoreEmptyParagraphs = ignoreEmptyParagraphs

        # El objeto Section actual en el cual estoy escribiendo.
        self._currentSection = None

        # Una lista de tuplas de dos elementos: un objeto Title, y un número con el nivel de heading. Utilizo
        # esta lista para formatear correctamente la toc.
        # En todoo momento, siempre el último elemento de la lista (la cima de la pila) contiene el último título
        # leído.
        self._titles = None

        # Representa cuál es, en un momento dado, el nivel de heading de primer nivel, es decir, el que vendría a ser
        # una entrada de primer nivel en la toc.
        # Puede darse una toc así:
        #               h3
        #               h3
        #           h2
        #           h2
        #       h1
        #       h1
        # Como se ve, los dos primeros h3 vendrían a ser en realidad h1, pero están corridos. Lo mismo con los h2. No
        # puedo suponer que los h1 van a ser siempre mi título de nivel 1. Incluso puede darse el caso de una toc que
        # no tenga h1, sino que absolutamente todos los títulos estén corridos.
        self._headingLevelBase = -1

        # Una lista de tuplas de dos elementos: el id de la nota en el docx (que utilizo luego para
        # obtener el contenido de la nota en footnotes.xml), y el nombre de la sección donde se hace
        # referencia a la nota.
        self._footnotesIdSection = None

        # Indica si se está procesando el contenido de todas las notas al pie o el del documento principal.
        self._isProcessingFootnotes = False

        # Un objeto EbookData.
        self._ebookData = None

        self._openDocx(inputFile)

    def convert(self):
        self._titles = []
        self._headingLevelBase = DocxConverter._MAX_HEADING_NUMBER + 1
        self._footnotesIdSection = []
        self._ebookData = ebook_data.EbookData()
        self._isProcessingFootnotes = False

        self._processDocument()

        if self._footnotesIdSection:
            self._isProcessingFootnotes = True
            self._processFootnotes()

        return self._ebookData

    def getRawText(self):
        docText = "".join(xml_utils.xpath(self._documentXml, "//w:t/text()", namespaces=utils.NAMESPACES))
        footnotesText = "".join(self._footnotes.getRawText()) if self._footnotes else ""

        return docText + footnotesText

    def _openDocx(self, inputFile):
        with zipfile.ZipFile(inputFile) as docx:
            contentTypesXml = etree.fromstring(docx.read("[Content_Types].xml"))

            path = '/ct:Types/ct:Override[@ContentType = "{0}"]/@PartName'

            docPath = xml_utils.xpath(contentTypesXml, path.format(DocxConverter._DOCUMENT_CONTENT_TYPE), namespaces=utils.NAMESPACES)[0]
            docPath = docPath.strip("/")
            self._documentXml = etree.fromstring(docx.read(docPath))

            stylesPath = xml_utils.xpath(contentTypesXml, path.format(DocxConverter._STYLES_CONTENT_TYPE), namespaces=utils.NAMESPACES)[0]
            self._styles = styles.Styles(docx.read(stylesPath.strip("/")))

            footnotesPath = xml_utils.xpath(contentTypesXml, path.format(DocxConverter._FOOTNOTES_CONTENT_TYPE), namespaces=utils.NAMESPACES)
            if footnotesPath:
                footnotesPath = footnotesPath[0].strip("/")

                footnotesDir, footnoteFileName = os.path.split(footnotesPath)
                footnotesRelsPath = footnotesDir + "/_rels/" + footnoteFileName + ".rels"

                try:
                    footnotesRels = docx.read(footnotesRelsPath)
                except KeyError:
                    footnotesRels = None

                self._footnotes = footnotes.Footnotes(docx.read(footnotesPath), footnotesRels)

            docDir, docFileName = os.path.split(docPath)
            docRelsPath = docDir + "/_rels/" + docFileName + ".rels"

            try:
                self._documentRelsXml = etree.fromstring(docx.read(docRelsPath))
            except KeyError:
                self._documentRelsXml = None

            for imgPath in [name for name in docx.namelist() if name.startswith(DocxConverter._MEDIA_FILES_PATH)]:
                self._mediaFiles[os.path.split(imgPath)[1]] = docx.read(imgPath)

    def _processDocument(self):
        self._currentSection = ebook_data.TextSection(0)

        body = xml_utils.find(self._documentXml, "w:body", utils.NAMESPACES)
        self._processMainContent(body)

        self._saveCurrentSection()

    def _processMainContent(self, node, tag="p"):
        """
        Procesa todos los párrafos y tablas de un nodo.

        @param node: un nodo lxml.
        @param tag: el tag a utilizar para los párrafos.
        """
        previousEmptyParagraphsCount = 0

        for child in node:
            if child.tag.endswith("}p"):
                hasParagraphText = utils.hasText(child)
                pageBreakPosition = utils.getPageBreakPosition(child)

                if pageBreakPosition == utils.PAGE_BREAK_ON_BEGINNING:
                    self._saveCurrentSection()

                if self._styles.hasParagraphHeadingStyle(child):
                    self._processHeading(child, hasParagraphText)
                else:
                    listLevel = utils.getListLevel(child)
                    if listLevel > -1:
                        self._processList(child, listLevel)
                    else:
                        self._processParagraph(child, hasParagraphText, tag, previousEmptyParagraphsCount)

                if pageBreakPosition == utils.PAGE_BREAK_ON_END:
                    self._saveCurrentSection()

                if hasParagraphText or pageBreakPosition != utils.NO_PAGE_BREAK:
                    previousEmptyParagraphsCount = 0
                else:
                    previousEmptyParagraphsCount += 1
            elif child.tag.endswith("}tbl"):
                self._processTable(child)

    def _processHeading(self, paragraph, hasText):
        if hasText:
            styleName = self._styles.getParagraphStyleName(paragraph)
            headingLevel = int(styleName.split(" ")[1])

            if headingLevel > 6:
                self._processParagraph(paragraph, hasText)
            else:
                # Los títulos en un docx no necesariamente está correctamente anidados: se puede tener un Título 1
                # seguido de un Titulo 3, por ejemplo. A medida que genero la toc, corrijo estos títulos, de manera
                # tal que en el ejemplo anterior, el Título 3 sea convertido a Título 2.

                titleText = xml_utils.getAllText(paragraph)

                if headingLevel < self._headingLevelBase:
                    self._headingLevelBase = headingLevel

                # Si es un heading de primer nivel, entonces ésta es una entrada en la toc de primer nivel.
                if headingLevel == self._headingLevelBase:
                    self._titles.clear()
                    title, titleId = self._ebookData.toc.addFirstLevelTitle(self._currentSection.name, titleText)
                else:
                    # Si el nivel de título actual es menor al anterior, debo sacar los títulos necesarios
                    # de mi pila para poner el título actual en el nivel que corresponde. Ejemplo:
                    #           1
                    #               2
                    #                   3
                    #                       4
                    # Dada una toc como la de arriba, si ahora tengo que insertar un título de nivel 2, debo ir
                    # comparando el 2 con cada uno de los niveles de títulos que están en la pila. Mientras mi
                    # título 2 sea menor o igual al que se encuentra en la pila, debo hacer un pop.
                    # De esta manera me queda en la cima de la pila el título padre en el cual debo insertar mi
                    # título 2 hijo.
                    if headingLevel < self._titles[-1][1]:
                        while headingLevel <= self._titles[-1][1]:
                            self._titles.pop()
                    # Si el nivel de título actual es igual al anterior procesado, significa que los títulos tienen el
                    # mismo padre, por lo que me basta hacer un solo pop en la pila para insertarlo en el lugar
                    # correcto. Ej:
                    #                   4
                    #                       5
                    # Si tengo que insertar un nuevo título 5 en la toc de arriba, debo sacar el título 5 de la
                    # cima de la pila para que quede el título 4 en la cima.
                    elif headingLevel == self._titles[-1][1]:
                        self._titles.pop()

                    title, titleId = self._ebookData.toc.addTitleToParent(self._titles[-1][0], self._currentSection.name, titleText)

                self._titles.append((title, headingLevel))

                # Dado que en la pila no tengo títulos repetidos (si el último título insertado era de nivel 4 y ahora
                # debo insertar otro de nivel 4, entonces hago un pop del título anterior e inserto el nuevo) la
                # cantidad de títulos que hay en la pila me da el nivel de anidamiento correcto para el título actual.
                fixedHeadingNumber = len(self._titles)

                self._currentSection.openHeading(fixedHeadingNumber, titleId)
                self._processParagraphContent(paragraph)
                self._currentSection.closeHeading(fixedHeadingNumber)

    def _processParagraph(self, paragraph, hasText, tag="p", previousEmptyParagraphsCount=0):
        isParagraphInsideDiv = False
        needToCloseDiv = False
        classValue = []

        customStyleName = self._styles.getParagaphCustomStyleName(paragraph)
        if customStyleName:
            previousParagraph = utils.getPreviousParagraph(paragraph)
            nextParagraph = utils.getNextParagraph(paragraph)

            styleId = self._styles.getParagraphStyleId(paragraph)
            previousParagraphStyleId = None
            nextParagraphStyleId = None

            if previousParagraph is not None:
                previousParagraphStyleId = self._styles.getParagraphStyleId(previousParagraph)

            if nextParagraph is not None:
                nextParagraphStyleId = self._styles.getParagraphStyleId(nextParagraph)

            if styleId != previousParagraphStyleId and styleId == nextParagraphStyleId:
                self._currentSection.openTag("div", **{"class": customStyleName})
                isParagraphInsideDiv = True
            elif styleId == previousParagraphStyleId:
                if styleId != nextParagraphStyleId:
                    needToCloseDiv = True
                isParagraphInsideDiv = True

        if hasText:
            if not self._ignoreEmptyParagraphs and previousEmptyParagraphsCount > 0:
                classValue.append("salto25" if previousEmptyParagraphsCount > 1 else "salto10")

            if customStyleName and not isParagraphInsideDiv:
                classValue.append(customStyleName)

            attributes = {"class": " ".join(classValue)} if classValue else {}

            self._currentSection.openTag(tag, **attributes)
            self._processParagraphContent(paragraph)
            self._currentSection.closeTag(tag)
        else:
            pic = utils.getPic(paragraph)
            if pic is not None:
                self._currentSection.openTag("p", **{"class": "ilustra"})
                self._processPic(pic)
                self._currentSection.closeTag("p")

        # Aun si el párrafo no tiene texto, debo cerrar el div que agrupa estilos si es necesario. Si no
        # lo hago, puede darse el caso de que el párrafo actual (sin texto) que estoy procesando tenga el
        # estilo X aplicado, y el párrafo anterior también, pero el párrafo siguiente no. Es decir, que el
        # párrafo actual debe cerrar el div, pero nunca lo voy a hacer si solamente cierro los divs cuando el
        # párrafo tiene texto.
        if needToCloseDiv:
            self._currentSection.closeTag("div")

    def _processParagraphContent(self, paragraph):
        previousRunFormats = []

        for child in paragraph:
            if child.tag.endswith("}r"):
                previousRunFormats = self._processRun(child, previousRunFormats)
            else:
                # Si de algún lado llame a este método que procesa el contenido de un párrafo, entonces
                # probablemente significa que dentro del nodo, en alguna parte hay texto, es decir, un
                # elemento w:t, y debo procesarlo.
                # Un párrafo (w:p) puede contener, además de w:r, w:hyperlink, w:smartag, etc., y todos
                # ellos pueden contener a su vez los mismos elementos que un w:p contiene, por lo que
                # me basta hacer un call recursivo para procesar este nodo, de manera tal que eventualmente
                # voy a terminar procesando los w:r que contienen el texto.
                self._processParagraphContent(child)

    def _processRun(self, run, previousRunFormats):
        styleId = self._styles.getRunStyleId(run)

        runFormats = utils.getRunFormats(run)

        # Si el run tiene aplicado un estilo, este estilo puede tener asociado formatos, por
        # ejemplo: negrita, cursiva, etc. Proceso también estos formatos.
        if styleId:
            for f in (f for f in self._styles.getStyleFormats(styleId) if f not in runFormats):
                runFormats.append(f)

        isLastRun = utils.getNextRun(run) is None
        needToCloseSpan = False

        self._processRunFormats(runFormats, previousRunFormats)

        if styleId:
            customStyleName = self._styles.getRunCustomStyleName(run)
            if customStyleName:
                previousRunStyleId = None
                nextRunStyleId = None

                previousRun = utils.getPreviousRun(run)
                nextRun = utils.getNextRun(run)

                if previousRun is not None:
                    previousRunStyleId = self._styles.getRunStyleId(previousRun)

                if nextRun is not None:
                    nextRunStyleId = self._styles.getRunStyleId(nextRun)

                if styleId != previousRunStyleId:
                    self._currentSection.openTag("span", **{"class": customStyleName})

                if styleId != nextRunStyleId:
                    needToCloseSpan = True

        for child in run:
            if child.tag.endswith("}t"):
                self._currentSection.appendText(child.text)
            elif child.tag.endswith("}footnoteReference"):
                footnoteId = xml_utils.xpath(run, "w:footnoteReference/@w:id", utils.NAMESPACES)[0]
                self._footnotesIdSection.append((footnoteId, self._currentSection.name))
                self._currentSection.insertNoteReference(len(self._footnotesIdSection))
            elif child.tag.endswith("}drawing"):
                pic = utils.getPic(child)
                if pic is not None:
                    self._processPic(pic)
            elif child.tag.endswith("}AlternateContent"):
                self._processAlternateContent(child)

        if isLastRun:
            for f in reversed(runFormats):
                self._currentSection.closeTag(f)

        if needToCloseSpan:
            self._currentSection.closeTag("span")

        return runFormats

    def _processText(self, node):
        self._currentSection.appendText(node.text)

    def _processList(self, paragraph, listLevel):
        previousParagraph = utils.getPreviousParagraph(paragraph)
        nextParagraph = utils.getNextParagraph(paragraph)

        previousParagraphListLevel = utils.getListLevel(previousParagraph) if previousParagraph is not None else -1
        nextParagraphListLevel = utils.getListLevel(nextParagraph) if nextParagraph is not None else -1

        if listLevel > previousParagraphListLevel:
            self._currentSection.openTag("ul")

        self._currentSection.openTag("li")
        self._processParagraphContent(paragraph)

        if nextParagraphListLevel == listLevel:
            self._currentSection.closeTag("li")
        elif nextParagraphListLevel < listLevel:
            self._currentSection.closeTag("li")

            # Cuando el siguiente nivel es menor al actual, debo cerrar los anidamientos correctamente.
            # Para saber cuántos anidamientos cerrar, solamente tengo que restarle al nivel actual el
            # siguiente (claro que supongo que los anidamientos son válidos...).
            # Si no hay próximo nivel (es decir, se termina la lista), entonces simplemente el nivel
            # actual me dice cuántos anidamientos debo cerrar.
            iterations = (listLevel - (nextParagraphListLevel if nextParagraphListLevel != -1 else 0))

            for i in range(iterations):
                self._currentSection.closeTag("ul")
                self._currentSection.closeTag("li")

            # Si la lista se termina, debo cerrar el primer "ul" de todos.
            if nextParagraphListLevel == -1:
                self._currentSection.closeTag("ul")

    def _processTable(self, table):
        self._currentSection.openTag("table", frame="box", rules="all")

        for child in table:
            if child.tag.endswith("tr"):
                self._currentSection.openTag("tr")

                for node in child:
                    if node.tag.endswith("tc"):
                        self._processMainContent(node, "td")

                self._currentSection.closeTag("tr")

        self._currentSection.closeTag("table")

    def _processRunFormats(self, runFormats, previousRunFormats):
        if runFormats != previousRunFormats:
            for f in reversed(previousRunFormats):
                self._currentSection.closeTag(f)

            for f in runFormats:
                self._currentSection.openTag(f)

    def _processFootnotes(self):
        self._currentSection = ebook_data.NotesSection()

        for footnoteId, footnoteSection in self._footnotesIdSection:
            footnote = self._footnotes.getFootnote(footnoteId)

            # Si bien dentro de una nota se encuentran párrafos y tablas y por lo tanto podría llamar
            # directamente al método processMainContent, estaría haciendo chequeos y comprobaciones innecesarias, ya
            # que, por ejemplo, una nota no puede tener saltos de página, ni tampoco necesito procesar títulos dentro
            # de una nota.
            self._processFootnote(footnote, footnoteSection)

        self._saveCurrentSection()

    def _processFootnote(self, footnote, footnoteSection):
        self._currentSection.openNote(footnoteSection)

        for child in footnote:
            if child.tag.endswith("}p"):
                hasText = utils.hasText(child)
                self._processParagraph(child, hasText)

        self._currentSection.closeNote()

    def _processPic(self, pic):
        rId = xml_utils.xpath(pic, "pic:blipFill/a:blip/@r:embed", utils.NAMESPACES)[0]
        self._addImageToCurrentSection(self._getImageName(rId))

    def _processAlternateContent(self, alternateContent):
        pathToTxbxContent = "mc:Choice/w:drawing/wp:inline/a:graphic/a:graphicData/wps:wsp/wps:txbx/w:txbxContent"
        txbxContent = xml_utils.find(alternateContent, pathToTxbxContent, utils.NAMESPACES)
        self._processMainContent(txbxContent, "span")

    def _saveCurrentSection(self):
        self._ebookData.addSection(self._currentSection)
        self._currentSection = ebook_data.TextSection(len(self._ebookData.sections))

    def _getImageName(self, rId):
        if not self._isProcessingFootnotes:
            imagePath = xml_utils.xpath(self._documentRelsXml, "rels:Relationship[@Id = '{0}']/@Target".format(rId), utils.NAMESPACES)[0]
            return os.path.split(imagePath)[1]
        else:
            return self._footnotes.getImageName(rId)

    def _addImageToCurrentSection(self, imageName):
        self._currentSection.appendImg(imageName)
        self._ebookData.addImage(imageName, self._mediaFiles[imageName])