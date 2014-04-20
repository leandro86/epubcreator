import os

from lxml import etree

from epubcreator.converters.docx import utils


class Footnotes:
    def __init__(self, footnotes, footnotesRels=None):
        self._footnotesXml = etree.parse(footnotes)
        self._footnotesRelsXml = etree.parse(footnotesRels) if footnotesRels else None

    def getFootnote(self, footnoteId):
        return utils.xpath(self._footnotesXml, 'w:footnote[@w:id = "{0}"]'.format(footnoteId))[0]

    def getImageName(self, rId):
        imagePath = utils.xpath(self._footnotesRelsXml, "rels:Relationship[@Id = '{0}']/@Target".format(rId))[0]
        return os.path.split(imagePath)[1]

    def getRawText(self):
        return "".join(utils.xpath(self._footnotesXml, "//w:t/text()"))
