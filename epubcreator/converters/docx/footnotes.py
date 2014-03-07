from lxml import etree

from epubcreator.converters import xml_utils
from epubcreator.converters.docx import utils


class Footnotes:
    def __init__(self, footnotesXml):
        self._footnotes = etree.XML(footnotesXml)

    def getFootnote(self, footnoteId):
        return xml_utils.xpath(self._footnotes,
                               'w:footnote[@w:id = "{0}"]'.format(footnoteId),
                               utils.NAMESPACES)[0]