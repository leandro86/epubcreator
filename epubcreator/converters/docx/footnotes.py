from lxml import etree

from epubcreator.converters import xml_utils
from epubcreator.converters.docx import utils


class Footnotes:
    def __init__(self, footnotesXml):
        self._footnotesXml = etree.XML(footnotesXml)

    def getFootnote(self, footnoteId):
        return xml_utils.xpath(self._footnotesXml,
                               'w:footnote[@w:id = "{0}"]'.format(footnoteId),
                               utils.NAMESPACES)[0]

    def getRawText(self):
        return "".join(xml_utils.xpath(self._footnotesXml, "//w:t/text()", namespaces=utils.NAMESPACES))
