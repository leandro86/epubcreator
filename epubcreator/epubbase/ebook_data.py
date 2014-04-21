import itertools

from lxml import etree

from epubcreator.epubbase import names


class EbookData:
    def __init__(self):
        self._textSections = []
        self._notesSections = []
        self._images = []
        self._headingsCount = 0
        self._notesReferences = []

    def createTextSection(self):
        return TextSection(self)

    def createNotesSection(self):
        return NotesSection(self)

    def addImage(self, imageName, imageContent):
        self._images.append(Image(imageName, imageContent))

    def iterTextSections(self):
        for section in self._textSections:
            yield section

    def iterNotesSections(self):
        for section in self._notesSections:
            yield section

    def iterAllSections(self):
        return itertools.chain(self.iterTextSections(), self.iterNotesSections())

    def iterImages(self):
        for image in self._images:
            yield image

    def countTextSections(self):
        return len(self._textSections)

    def countNotesSections(self):
        return len(self._notesSections)

    ### #################################################################################### ###
    ### Métodos visibles solamente a este módulo, con el único fin de ser usados por Section ###
    ### #################################################################################### ###
    def _addTextSection(self, section):
        self._textSections.append(section)

    def _addNotesSection(self, section):
        self._notesSections.append(section)

    def _getHeadingId(self):
        self._headingsCount += 1
        return "heading_id_{0}".format(self._headingsCount)

    def _addNoteReference(self, sectionName):
        self._notesReferences.append(sectionName)

    def _countNotesReferences(self):
        return len(self._notesReferences)

    def _getNoteReference(self, i):
        return self._notesReferences[i]


class Section:
    _DOCTYPE = ('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"'
                ' "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">')

    _TEXT = 0
    _TAIL = 1

    def __init__(self, ebookData):
        self._ebookData = ebookData

        self.name = self._generateSectionName()
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

    def openHeading(self, level, hasIdAttr=True):
        tag = "h{0}".format(level)
        if hasIdAttr:
            self.openTag(tag, id=self._ebookData._getHeadingId())
        else:
            self.openTag(tag)

    def closeHeading(self, level):
        tag = "h{0}".format(level)
        self.closeTag(tag)

    def appendImg(self, imageName):
        self.openTag("img", alt="", src="../Images/{0}".format(imageName))
        self.closeTag("img")

    def xpath(self, expr):
        return self._html.xpath(expr)

    def toHtml(self):
        return etree.tostring(self._html, xml_declaration=True, pretty_print=True, encoding="utf-8", doctype=Section._DOCTYPE)

    def toRawText(self):
        text = self._html.xpath("//text()")
        return "".join(text)

    def save(self):
        raise NotImplemented

    def _generateSectionName(self):
        raise NotImplemented

    def _writeTextBuffer(self):
        text = "".join(self._textBuffer)

        if self._textWritePos == Section._TEXT:
            self._lastElement.text = text
        else:
            self._lastElement.tail = text

        self._textBuffer = []


class TextSection(Section):
    def __init__(self, ebookData):
        super().__init__(ebookData)

    def insertNoteReference(self):
        self._ebookData._addNoteReference(self.name)
        noteNumber = self._ebookData._countNotesReferences()

        self.openTag("a", id="rf{0}".format(noteNumber), href="../Text/notas.xhtml#nt{0}".format(noteNumber))
        self.openTag("sup")
        self.appendText("[{0}]".format(str(noteNumber)))
        self.closeTag("sup")
        self.closeTag("a")

    def save(self):
        self._ebookData._addTextSection(self)

    def toRawText(self):
        # Debo ignorar las referencias a las notas al pie.
        text = self._html.xpath("//*[not(self::sup[parent::a[starts-with(@id, 'rf')]])]/text()")
        return "".join(text)

    def _generateSectionName(self):
        return names.generateTextSectionName(self._ebookData.countTextSections() + 1)


class NotesSection(Section):
    def __init__(self, ebookData):
        super().__init__(ebookData)

        self._footnotesCount = 0
        self._hasCurrentFootnoteContent = True

        self.openHeading(1, hasIdAttr=False)
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

    def openNote(self):
        """
        Este método, junto con closeNote, están íntimamente relacionados con insertNoteReference.
        La primer llamada a openNote y closeNote se corresponde con la primer llamada a insertNoteReference, y es
        de allí de donde se obtiene el nombre de la sección donde se encuentra la referencia a la nota. Lo mismo
        para la segunda llamada a openNote y closeNote, etc. De lo que se deduce que primero debe insertarse
        la referecia a la nota a través de insertNoteReference, y luego llamar a openNote y closeNote.
        """
        super().openTag("div", **{"class": "nota"})

        self._footnotesCount += 1
        self._hasCurrentFootnoteContent = False

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

        sectionName = self._ebookData._getNoteReference(self._footnotesCount - 1)
        anchor = etree.Element("a", href="../Text/{0}#rf{1}".format(sectionName, self._footnotesCount))
        anchor.text = "<<"

        self._lastElement.append(anchor)
        self.closeTag("div")

    def save(self):
        self._ebookData._addNotesSection(self)

    def toRawText(self):
        # Debo obviar el título "Notas", el texto del primer superíndice y el texto del link de retorno.
        text = self._html.xpath("//*[not(self::a) and "
                                "not(. = ./parent::*[starts-with(@id, 'nt')]/child::sup[1]) and "
                                ". != /html/body/child::*[1]]/text()")
        return "".join(text)

    def _generateSectionName(self):
        return names.NOTES_FILENAME


class Image:
    def __init__(self, name, content):
        self.name = name
        self.content = content

    def __str__(self):
        return self.name


class CloseTagMismatchError(Exception):
    def __init__(self, expected, got):
        self.expected = expected
        self.got = got

    def __str__(self):
        return "Se esperaba tag de cierre '{0}', pero se encontró '{1}'.".format(self.expected, self.got)