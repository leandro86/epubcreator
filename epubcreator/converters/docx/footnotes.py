from lxml import etree

from epubcreator.converters.docx import utils


class Footnotes:
    def __init__(self, footnotes):
        self._footnotesXml = etree.parse(footnotes)

    def getFootnote(self, footnoteId):
        return utils.xpath(self._footnotesXml, 'w:footnote[@w:id = "{0}"]'.format(footnoteId))[0]

    def getRawText(self):
        return "".join(utils.xpath(self._footnotesXml, "//w:t/text()"))