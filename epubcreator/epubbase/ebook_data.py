from lxml import etree

from epubcreator.epubbase import epubbase_names


class EbookData:
    def __init__(self):
        # Lista de Section.
        self.sections = []

        # Lista de Image.
        self.images = []

        # Un objeto Toc.
        self.toc = Toc()

    def addSection(self, section):
        self.sections.append(section)

    def addImage(self, imageName, imageContent):
        self.images.append(Image(imageName, imageContent))


class Section:
    _DOCTYPE = ('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"'
                ' "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">')

    _TEXT = 0
    _TAIL = 1

    def __init__(self, sectionNumber):
        self.name = self._generateSectionName(sectionNumber)

        self._html = etree.Element("html", xmlns="http://www.w3.org/1999/xhtml")

        head = etree.Element("head")
        head.append(etree.Element("title"))
        head.append(etree.Element("link", href="../Styles/style.css", rel="stylesheet", type="text/css"))

        self._html.append(head)

        body = etree.Element("body")

        self._html.append(body)

        # Una pila que contiene los elementos abiertos anidados. La necesito para saber en qué
        # elemento debo escribir el texto.
        self._openedElements = [body]

        # El último elemento en ser abierto o cerrado. Representa el elemento en el cual debo
        # escribir el texto cuando sea necesario.
        self._lastElement = body

        # Tener el último elemento en ser abierto o cerrado no me basta, sino que necesito saber
        # en qué posición debo escribir: text o tail, ya que lxml hace esta diferencia.
        self._textWritePos = Section._TEXT

        # El texto propiamente dicho de cada nodo. Solamente lo vuelco al nodo (ya sea en su
        # atributo text o tail) al momento de abrir o cerrar otro nodo.
        self._textBuffer = []

    def appendText(self, text):
        self._textBuffer.append(text)

    def openTag(self, tag, **attributes):
        self._writeTextBuffer()

        e = etree.Element(tag, **attributes)

        self._openedElements[-1].append(e)
        self._openedElements.append(e)

        self._lastElement = e
        self._textWritePos = Section._TEXT

    def closeTag(self, tag):
        e = self._openedElements[-1]

        if e.tag != tag:
            raise CloseTagMismatchError(e.tag, tag)

        self._writeTextBuffer()
        self._openedElements.pop()

        self._lastElement = e
        self._textWritePos = Section._TAIL

    def openHeading(self, level, headingId=None):
        tag = "h{0}".format(level)
        if headingId:
            self.openTag(tag, id=headingId)
        else:
            self.openTag(tag)

    def closeHeading(self, level):
        tag = "h{0}".format(level)
        self.closeTag(tag)

    def appendImg(self, imageName):
        self.openTag("img", alt="", src="../Images/{0}".format(imageName))
        self.closeTag("img")

    def toHtml(self):
        return etree.tostring(self._html, xml_declaration=True, pretty_print=True, encoding="utf-8", doctype=Section._DOCTYPE)

    def toRawText(self):
        text = self._html.xpath("//text()")
        return "".join(text)

    def _generateSectionName(self, sectionNumber):
        raise NotImplemented

    def _writeTextBuffer(self):
        text = "".join(self._textBuffer)

        if self._textWritePos == Section._TEXT:
            self._lastElement.text = text
        else:
            self._lastElement.tail = text

        self._textBuffer = []


class TextSection(Section):
    def __init__(self, sectionNumber):
        super().__init__(sectionNumber)

    def insertNoteReference(self, noteNumber):
        self.openTag("a", id="rf{0}".format(noteNumber), href="../Text/notas.xhtml#nt{0}".format(noteNumber))
        self.openTag("sup")
        self.appendText("[{0}]".format(str(noteNumber)))
        self.closeTag("sup")
        self.closeTag("a")

    def toRawText(self):
        # Debo ignorar las referencias a las notas al pie.
        text = self._html.xpath("//*[not(self::sup[parent::a[starts-with(@id, 'rf')]])]/text()")
        return "".join(text)

    def _generateSectionName(self, sectionNumber):
        return epubbase_names.generateTextSectionName(sectionNumber)


class NotesSection(Section):
    def __init__(self, sectionNumber=0):
        super().__init__(sectionNumber)

        self._footnotesCount = 0
        self._currentFootnoteSection = ""
        self._hasCurrentFootnoteContent = True

        self.openHeading(1)
        self.appendText("Notas")
        self.closeHeading(1)

    def openTag(self, tag, **attributes):
        if not self._hasCurrentFootnoteContent:
            attributes["id"] = "nt{0}".format(self._footnotesCount)

            super().openTag(tag, **attributes)
            super().openTag("sup")
            self.appendText("[{0}]".format(self._footnotesCount))
            super().closeTag("sup")

            self._hasCurrentFootnoteContent = True
        else:
            super().openTag(tag, **attributes)

    def openNote(self, footnoteSection):
        super().openTag("div", **{"class": "nota"})

        self._currentFootnoteSection = footnoteSection
        self._hasCurrentFootnoteContent = False
        self._footnotesCount += 1

    def closeNote(self):
        # Debe haber un espacio antes del link de retorno, y debo escribirlo en el nodo correcto.
        # Al cerrar la nota, lo único que sé es que _lastElement contiene el último elemento en ser cerrado
        # y por ende, es el elemento donde debo insertar el tag "a". Ahora, dependiendo de si dicho elemento
        # tiene hijos o no, escribo el texto donde corresponda.
        children = list(self._lastElement)

        if children:
            lastChild = children[-1]

            if lastChild.tail:
                lastChild.tail += " "
            else:
                lastChild.tail = " "
        else:
            if self._lastElement.text:
                self._lastElement.text += " "
            else:
                self._lastElement.text = " "

        anchor = etree.Element("a", href="../Text/{0}#rf{1}".format(self._currentFootnoteSection, self._footnotesCount))
        anchor.text = "<<"

        self._lastElement.append(anchor)
        self.closeTag("div")

    def toRawText(self):
        # Debo obviar el título "Notas", el texto del primer superíndice y el texto del link de retorno.
        text = self._html.xpath("//*[not(self::a) and "
                                "not(. = ./parent::*[starts-with(@id, 'nt')]/child::sup[1]) and "
                                ". != /html/body/child::*[1]]/text()")
        return "".join(text)

    def _generateSectionName(self, sectionNumber):
        return epubbase_names.NOTES_FILENAME


class Image:
    def __init__(self, name, content):
        self.name = name
        self.content = content


class Toc:
    def __init__(self):
        self.titles = []
        self._titlesCount = 0

    def addFirstLevelTitle(self, sectionName, titleText, generateId=True):
        self._titlesCount += 1

        title, titleId = self._createTitle(sectionName, titleText, generateId)
        self.titles.append(title)

        return title, titleId

    def addTitleToParent(self, parentTitle, sectionName, titleText, generateId=True):
        self._titlesCount += 1

        title, titleId = self._createTitle(sectionName, titleText, generateId)
        parentTitle.addTitle(title)

        return title, titleId

    def getTotalTitlesCount(self):
        return self._titlesCount

    def getFirstLevelTitlesCount(self):
        return len(self.titles)

    def _createTitle(self, sectionName, titleText, generateId=True):
        titleLocation = sectionName
        titleId = None

        if generateId:
            titleId = "heading_id_{0}".format(self._titlesCount)
            titleLocation += "#{0}".format(titleId)

        title = Title(titleLocation, titleText)
        return title, titleId


class Title:
    def __init__(self, titleLocation, titleText):
        self.titleLocation = titleLocation
        self.text = titleText
        self.childTitles = []

    def addTitle(self, title):
        self.childTitles.append(title)


class CloseTagMismatchError(Exception):
    def __init__(self, expected, got):
        self.expected = expected
        self.got = got

    def __str__(self):
        return "Se esperaba tag de cierre '{0}', pero se encontró '{1}'.".format(self.expected, self.got)