import os

from lxml import etree

from epubcreator.converters import converter_base
from epubcreator.epubbase import ebook_data
from epubcreator.converters.docx import utils, styles, footnotes, docx
from epubcreator.misc.options import Option


class DocxConverter(converter_base.AbstractConverter):
    FILE_TYPE = "docx"
    OPTIONS = [Option(name="ignoreEmptyParagraphs",
                      value=True,
                      description='Indica si los párrafos en blanco deben ignorarse, o reemplazarse por la clase '
                                  '"salto" de acuerdo al siguiente criterio: un párrafo en blanco, se reemplaza por la '
                                  'clase "salto10"; dos o más, por la clase "salto25".')]

    _MAX_HEADING_NUMBER = 6

    def __init__(self, inputFilePath, **options):
        super().__init__(inputFilePath, **options)

        self._docx = docx.Docx(inputFilePath)

        self._documentXml = etree.parse(self._docx.document())
        self._styles = styles.Styles(self._docx.styles()) if self._docx.hasStyles() else None
        self._footnotes = footnotes.Footnotes(self._docx.footnotes()) if self._docx.hasFootnotes() else None

        # Contiene el nombre de las imágenes que ya fueron agregadas al ebook.
        self._images = set()

        # El objeto Section actual en el cual estoy escribiendo.
        self._currentSection = None

        # Una lista de números con los niveles de heading. Utilizo esta lista para corregir el anidamiento de headings
        # en el docx. En todoo momento, siempre el último elemento de la lista (la cima de la pila) contiene el último título leído.
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

        # Una lista con los ids de las notas en el docx (que utilizo luego para obtener el contenido de la nota en footnotes.xml).
        self._footnotesId = None

        # Indica si se está procesando el contenido de todas las notas al pie o el del documento principal.
        self._isProcessingFootnotes = False

        # Un objeto EbookData.
        self._ebookData = None

    def convert(self):
        self._titles = []
        self._headingLevelBase = DocxConverter._MAX_HEADING_NUMBER + 1
        self._footnotesId = []
        self._ebookData = ebook_data.EbookData()
        self._isProcessingFootnotes = False
        self._images = set()

        self._processDocument()

        if self._footnotesId:
            self._isProcessingFootnotes = True
            self._processFootnotes()

        return self._ebookData

    def getRawText(self):
        docText = "".join(utils.xpath(self._documentXml, "//w:t/text()"))
        footnotesText = "".join(self._footnotes.getRawText()) if self._footnotes else ""

        return docText + footnotesText

    def _processDocument(self):
        self._currentSection = self._ebookData.createTextSection()

        body = utils.find(self._documentXml, "w:body")
        self._processMainContent(body)

        self._currentSection.save()

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
                    self._currentSection.save()
                    self._currentSection = self._ebookData.createTextSection()

                if self._styles.hasParagraphHeadingStyle(child):
                    self._processHeading(child, hasParagraphText)
                else:
                    listLevel = utils.getListLevel(child)
                    if listLevel > -1:
                        self._processList(child, listLevel)
                    else:
                        self._processParagraph(child, hasParagraphText, tag, previousEmptyParagraphsCount)

                if pageBreakPosition == utils.PAGE_BREAK_ON_END:
                    self._currentSection.save()
                    self._currentSection = self._ebookData.createTextSection()

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
                if headingLevel < self._headingLevelBase:
                    self._headingLevelBase = headingLevel

                # Si es un heading de primer nivel, entonces ésta es una entrada en la toc de primer nivel.
                if headingLevel == self._headingLevelBase:
                    self._titles.clear()
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
                    if headingLevel < self._titles[-1]:
                        while headingLevel <= self._titles[-1]:
                            self._titles.pop()
                    # Si el nivel de título actual es igual al anterior procesado, significa que los títulos tienen el
                    # mismo padre, por lo que me basta hacer un solo pop en la pila para insertarlo en el lugar
                    # correcto. Ej:
                    #                   4
                    #                       5
                    # Si tengo que insertar un nuevo título 5 en la toc de arriba, debo sacar el título 5 de la
                    # cima de la pila para que quede el título 4 en la cima.
                    elif headingLevel == self._titles[-1]:
                        self._titles.pop()

                self._titles.append(headingLevel)

                # Dado que en la pila no tengo títulos repetidos (si el último título insertado era de nivel 4 y ahora
                # debo insertar otro de nivel 4, entonces hago un pop del título anterior e inserto el nuevo) la
                # cantidad de títulos que hay en la pila me da el nivel de anidamiento correcto para el título actual.
                fixedHeadingNumber = len(self._titles)

                self._currentSection.openHeading(fixedHeadingNumber)
                self._processParagraphContent(paragraph)
                self._currentSection.closeHeading(fixedHeadingNumber)

    def _processParagraph(self, paragraph, hasText, tag="p", previousEmptyParagraphsCount=0):
        isParagraphInsideDiv = False
        needToCloseDiv = False
        classValue = []

        className = self._styles.getParagraphClassName(paragraph)
        if className:
            previousParagraph = self._getPreviousParagraph(paragraph)
            nextParagraph = self._getNextParagraph(paragraph)

            styleId = self._styles.getParagraphStyleId(paragraph)
            previousParagraphStyleId = None
            nextParagraphStyleId = None

            if previousParagraph is not None:
                previousParagraphStyleId = self._styles.getParagraphStyleId(previousParagraph)

            if nextParagraph is not None:
                nextParagraphStyleId = self._styles.getParagraphStyleId(nextParagraph)

            if styleId != previousParagraphStyleId and styleId == nextParagraphStyleId:
                self._currentSection.openTag("div", **{"class": className})
                isParagraphInsideDiv = True
            elif styleId == previousParagraphStyleId:
                if styleId != nextParagraphStyleId:
                    needToCloseDiv = True
                isParagraphInsideDiv = True

        if hasText:
            if not self._options.ignoreEmptyParagraphs and previousEmptyParagraphsCount > 0:
                classValue.append("salto25" if previousEmptyParagraphsCount > 1 else "salto10")

            if className and not isParagraphInsideDiv:
                classValue.append(className)

            attributes = {"class": " ".join(classValue)} if classValue else {}

            self._currentSection.openTag(tag, **attributes)
            self._processParagraphContent(paragraph)
            self._currentSection.closeTag(tag)
        else:
            imagesId = utils.getImagesId(paragraph)

            if imagesId:
                if len(imagesId) == 1:
                    self._currentSection.openTag("p", **{"class": "ilustra"})
                    self._processImage(imagesId[0])
                    self._currentSection.closeTag("p")
                else:
                    # Si hay varias imágenes en un mismo párrafo que no contiene texto, entonces
                    # simplemente las agrego una detrás de otra.
                    self._currentSection.openTag("p")

                    for imageId in imagesId:
                        self._processImage(imageId)

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
        isLastRun = utils.getNextRun(run) is None
        needToCloseSpan = False
        needToOpenSpan = False
        className = ""

        # Si el run tiene aplicado un estilo, este estilo puede tener asociado formatos, por
        # ejemplo: negrita, cursiva, etc. Proceso también estos formatos.
        if styleId:
            formats = runFormats + utils.getRunDisabledFormats(run)
            for f in (f for f in self._styles.getStyleFormats(styleId) if f not in formats):
                runFormats.append(f)

            className = self._styles.getRunClassName(run)

            if className:
                previousRunStyleId = None
                nextRunStyleId = None

                previousRun = utils.getPreviousRun(run)
                nextRun = utils.getNextRun(run)

                if previousRun is not None:
                    previousRunStyleId = self._styles.getRunStyleId(previousRun)

                if nextRun is not None:
                    nextRunStyleId = self._styles.getRunStyleId(nextRun)

                if styleId != previousRunStyleId:
                    needToOpenSpan = True

                if styleId != nextRunStyleId:
                    needToCloseSpan = True

        # Cada vez que tengo que abrir un span porque es necesario incluir un estilo
        # propio, entonces cierro absolutamente todos los tags de formato que estén abiertos.
        # Supongamos que tengo este texto:
        #   <strong>aaaaa<span>aaaabbbb</span></strong>
        # Ahora, quiero cerrar el "strong" al comienzo de "bbbb". Para ello tengo dos
        # opciones:
        #   1- <strong>aaaaa<span>aaaa</span></strong><span>bbbb</span>
        #   2- <strong>aaaaa</strong><span><strong>aaaa</strong>bbbb</span>
        # En la primera, lo que cierro y abro son los spans; en la segunda, son
        # los strongs. Yo opté implementar la segunda opción.
        # Ahora bien, puede suceder lo siguiente. Supongamos este texto:
        #   aaaaaaaaaaa<span>bbbbbbb</span>cccccccccccc
        # Si ese texto tuviera aplicado negrita desde el comienzo hasta el final, lo
        # óptimo sería hacer:
        #   <strong>aaaaaaaaaaa<span>bbbbbbb</span>cccccccccccc</strong>
        # Sin embargo, dado que cierro todos los tags antes del comienzo de un span, resulta
        # esto:
        #   <strong>aaaaaaaaaaa</strong><span><strong>bbbbbbb</strong></span><strong>cccccccccccc</strong>
        # El problema es que de antemano no puedo saber hasta donde se extiende el strong, porque tal vez
        # tenga que cerrarlo en medio de un span, como en el ejemplo anterior, y entonces debo cerrar primero
        # el span, luego el strong, y luego abrir el span de vuelta, para no causar un error de anidamiento.
        # Creo que está bien dejarlo así (es decir, abrir y cerrar la menor cantidad de spans posiles), porque
        # de todas maneras es más fácil para el browser procesar varios strongs (o cualquier otro
        # tag de formato, como em) que varios spans con una clase.
        if runFormats != previousRunFormats or needToOpenSpan:
            for f in reversed(previousRunFormats):
                self._currentSection.closeTag(f)

            # Dado el caso de un run que contenga un estilo y formatos, entonces abro
            # el span primero, y dentro del span abro los formatos.
            if needToOpenSpan:
                self._currentSection.openTag("span", **{"class": className})

            for f in runFormats:
                self._currentSection.openTag(f)

        for child in run:
            if child.tag.endswith("}t"):
                self._currentSection.appendText(child.text)
            elif child.tag.endswith("}footnoteReference"):
                footnoteId = utils.xpath(run, "w:footnoteReference/@w:id")[0]
                self._footnotesId.append(footnoteId)
                self._currentSection.insertNoteReference()
            elif child.tag.endswith("}drawing") or child.tag.endswith("}pict"):
                imagesId = utils.getImagesId(child)
                if imagesId:
                    self._processImage(imagesId[0])
            elif child.tag.endswith("}br") and not child.attrib:
                self._currentSection.openTag("br")
                self._currentSection.closeTag("br")
            elif child.tag.endswith("}AlternateContent"):
                self._processAlternateContent(child)

        if needToCloseSpan:
            # No puedo simplemente cerrar el span, porque puede haber tags de formato abiertos
            # dentro del span: necesito cerrar esos tags primero.
            isSpanClosed = False
            while not isSpanClosed:
                try:
                    self._currentSection.closeTag("span")
                    isSpanClosed = True
                except ebook_data.CloseTagMismatchError as e:
                    self._currentSection.closeTag(e.expected)

            # Dado que cuando abro un span cierro todos los tags de formato, puedo asumir
            # que todos los tags de formato que cerré arriba eran todos los que estaban en
            # runFormats. Ahora bien, como al cerrar el span cerré todos los tags de formato, eso
            # significa que desde el punto de vista del run siguiente, no hay tags de formatos previos
            # abiertos, por eso debo retornar una lista vacía de formatos.
            runFormats = []
        elif isLastRun:
            for f in reversed(runFormats):
                self._currentSection.closeTag(f)

        return runFormats

    def _processList(self, paragraph, listLevel):
        previousParagraph = self._getPreviousParagraph(paragraph)
        nextParagraph = self._getNextParagraph(paragraph)

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
                        if utils.hasText(node):
                            paragraphsCount = utils.xpath(node, "count(w:p)")

                            # Uso el tag "p" si hay más de un párrafo.
                            if paragraphsCount > 1:
                                self._currentSection.openTag("td")
                                self._processMainContent(node, "p")
                                self._currentSection.closeTag("td")
                            else:
                                self._processMainContent(node, "td")
                        else:
                            # No puedo ignorar la celda si no tiene texto!
                            self._currentSection.openTag("td")
                            self._currentSection.closeTag("td")

                self._currentSection.closeTag("tr")

        self._currentSection.closeTag("table")

    def _processFootnotes(self):
        self._currentSection = self._ebookData.createNotesSection()

        for footnoteId in self._footnotesId:
            footnote = self._footnotes.getFootnote(footnoteId)

            # Si bien dentro de una nota se encuentran párrafos y tablas y por lo tanto podría llamar
            # directamente al método processMainContent, estaría haciendo chequeos y comprobaciones innecesarias, ya
            # que, por ejemplo, una nota no puede tener saltos de página, ni tampoco necesito procesar títulos dentro
            # de una nota.
            self._processFootnote(footnote)

        self._currentSection.save()

    def _processFootnote(self, footnote):
        self._currentSection.openNote()

        for child in footnote:
            if child.tag.endswith("}p"):
                hasText = utils.hasText(child)
                self._processParagraph(child, hasText)
            elif child.tag.endswith("}tbl"):
                self._processTable(child)

        self._currentSection.closeNote()

    def _processImage(self, imageId):
        imageFullName = self._docx.documentTarget(imageId) if not self._isProcessingFootnotes else self._docx.footnotesTarget(imageId)
        imageName = os.path.split(imageFullName)[-1]

        self._currentSection.appendImg(imageName)

        if not imageName in self._images:
            self._ebookData.addImage(imageName, self._docx.read(imageFullName))
            self._images.add(imageName)

    def _processAlternateContent(self, alternateContent):
        pathToTxbxContent = "mc:Choice/w:drawing/wp:inline/a:graphic/a:graphicData/wps:wsp/wps:txbx/w:txbxContent"
        txbxContent = utils.find(alternateContent, pathToTxbxContent)
        self._processMainContent(txbxContent, "span")

    def _getNextParagraph(self, paragraph):
        # Debo tener en cuenta los saltos de página en este método. Si el párrafo
        # en cuestión tiene un salto de página al final, o el párrafo siguiente lo tiene
        # al principio, significa que el párrafo siguiente va a ir en una nueva sección, por lo
        # que desde el punto de vista del párrafo actual, no hay ningún párrafo siguiente, y no
        # debo retornar nada. De no tener en cuenta esto, algunos tags pueden no cerrarse o abrirse
        # correctamente, como por ejemplo, las listas, que necesitan examinar el párrafo anterior y
        # siguiente al actual. Un razonamiento similar se aplica para el método getPreviousParagraph().
        nextP = utils.getNextParagraph(paragraph)

        if nextP is not None:
            nextPBrPos = utils.getPageBreakPosition(nextP)
            currentPBrPos = utils.getPageBreakPosition(paragraph)

            return nextP if nextPBrPos != utils.PAGE_BREAK_ON_BEGINNING and currentPBrPos != utils.PAGE_BREAK_ON_END else None
        else:
            return None

    def _getPreviousParagraph(self, paragraph):
        previousP = utils.getPreviousParagraph(paragraph)

        if previousP is not None:
            previousPBrPos = utils.getPageBreakPosition(previousP)
            currentPBrPos = utils.getPageBreakPosition(paragraph)

            return previousP if previousPBrPos != utils.PAGE_BREAK_ON_END and currentPBrPos != utils.PAGE_BREAK_ON_BEGINNING else None
        else:
            return None