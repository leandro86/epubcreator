from lxml import etree


class Toc:
    _TOC_NS = "http://www.daisy.org/z3986/2005/ncx/"

    def __init__(self, tocContent):
        """
        @param tocContent: un string con el contenido de toc.ncx.
        """
        self._toc = etree.fromstring(tocContent)

    def getTitles(self):
        navMap = self._xpath(self._toc, "/toc:ncx/toc:navMap")[0]
        titles = []

        for navPoint in navMap:
            text = self._xpath(navPoint, "toc:navLabel/toc:text/text()")[0]
            src = self._xpath(navPoint, "toc:content/@src")[0]
            titles.append((text, src))

        return titles

    def _xpath(self, element, xpath):
        return element.xpath(xpath, namespaces={"toc": Toc._TOC_NS})