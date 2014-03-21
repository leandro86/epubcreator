import os

from lxml import etree

from epubcreator.converters import xml_utils
from epubcreator.converters.docx import utils


class Footnotes:
    def __init__(self, footnotes, footnotesRels=None):
        self._footnotesXml = etree.fromstring(footnotes)
        self._footnotesRelsXml = etree.fromstring(footnotesRels) if footnotesRels else None

    def getFootnote(self, footnoteId):
        return xml_utils.xpath(self._footnotesXml, 'w:footnote[@w:id = "{0}"]'.format(footnoteId), utils.NAMESPACES)[0]

    def getImageName(self, rId):
        imagePath = xml_utils.xpath(self._footnotesRelsXml, "rels:Relationship[@Id = '{0}']/@Target".format(rId), utils.NAMESPACES)[0]
        return os.path.split(imagePath)[1]

    def getRawText(self):
        return "".join(xml_utils.xpath(self._footnotesXml, "//w:t/text()", namespaces=utils.NAMESPACES))
