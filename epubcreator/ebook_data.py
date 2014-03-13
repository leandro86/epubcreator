import lxml.html

from epubcreator import epubbase_names


class EbookData:
    def __init__(self):
        # Lista de Section
        self.sections = []

        # Lista de Image
        self.images = []

        # Un objeto Toc
        self.toc = Toc()

    def addSection(self, section):
        self.sections.append(section)

    def addImage(self, imageName, imageContent):
        self.images.append(Image(imageName, imageContent))


class Section:
    _DOCTYPE = ('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"'
                ' "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">')
    _XML_DECLARATION = '<?xml version="1.0" encoding="utf-8" standalone="no"?>'
    _HTML_HEAD = '<head><title></title><link href="../Styles/style.css" rel="stylesheet" type="text/css" /></head>'
    _HTML_OPENTAG = '<html xmlns="http://www.w3.org/1999/xhtml">'

    def __init__(self, sectionNumber):
        self.name = self._generateSectionName(sectionNumber)
        self._content = []

    def appendText(self, text):
        self._content.append(text)

    def openTag(self, tag, attributes=None):
        self.appendText(self._generateOpenTag(tag, attributes))

    def closeTag(self, tag):
        self.appendText(self._generateCloseTag(tag))

    def openHeading(self, level, headingId=None):
        tag = "h{0}".format(level)
        attributes = dict(id=headingId) if headingId else None
        self.openTag(tag, attributes)

    def closeHeading(self, level):
        tag = "h{0}".format(level)
        self.closeTag(tag)

    def appendImg(self, imageName):
        self.openTag("img", dict(alt="", src="../Images/{0}".format(imageName)))
        self.closeTag("img")

    def toHtml(self):
        html = "".join((Section._XML_DECLARATION,
                        Section._DOCTYPE,
                        Section._HTML_OPENTAG,
                        Section._HTML_HEAD,
                        self._generateOpenTag("body"),
                        "".join(self._content),
                        self._generateCloseTag("body"),
                        self._generateCloseTag("html")))

        return html

    def toRawText(self):
        return lxml.html.fromstring("".join(self._content)).text_content()

    def _generateOpenTag(self, tag, attributes=None):
        if attributes is None:
            return "<{0}>".format(tag)
        else:
            attr = " ".join(['{0}="{1}"'.format(k, v) for k, v in attributes.items()])
            return "<{0} {1}>".format(tag, attr)

    def _generateCloseTag(self, tag):
        return "</{0}>".format(tag)

    def _generateSectionName(self, sectionNumber):
        raise NotImplemented


class TextSection(Section):
    def __init__(self, sectionNumber):
        super().__init__(sectionNumber)

    def insertNoteReference(self, noteNumber):
        self.openTag("a", dict(id="rf{0}".format(noteNumber), href="../Text/notas.xhtml#nt{0}".format(noteNumber)))
        self.openTag("sup")
        self.appendText("[{0}]".format(str(noteNumber)))
        self.closeTag("sup")
        self.closeTag("a")

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

    def openTag(self, tag, attributes=None):
        if not self._hasCurrentFootnoteContent:
            attributes = attributes or {}
            attributes["id"] = "nt{0}".format(self._footnotesCount)

            super().openTag(tag, attributes)
            super().openTag("sup")
            self.appendText("[{0}]".format(self._footnotesCount))
            super().closeTag("sup")

            self._hasCurrentFootnoteContent = True
        else:
            super().openTag(tag, attributes)

    def openNote(self, footnoteSection):
        super().openTag("div", {"class": "nota"})

        self._currentFootnoteSection = footnoteSection
        self._hasCurrentFootnoteContent = False
        self._footnotesCount += 1

    def closeNote(self):
        pos = len(self._content) - 1
        returnLink = '<a href="../Text/{0}#rf{1}">&lt;&lt;</a>'.format(self._currentFootnoteSection,
                                                                       self._footnotesCount)
        self._content.insert(pos, returnLink)

        self.closeTag("div")

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