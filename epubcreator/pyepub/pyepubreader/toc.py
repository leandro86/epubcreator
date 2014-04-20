import os
from lxml import etree


class Toc:
    _TOC_NS = "http://www.daisy.org/z3986/2005/ncx/"

    def __init__(self, toc):
        self._toc = etree.parse(toc)

    def getTitles(self):
        def addTitles(parentNavPoint):
            titles = []

            childNavPoints = self._xpath(parentNavPoint, "toc:navPoint")
            for navPoint in childNavPoints:
                text = self._xpath(navPoint, "toc:navLabel/toc:text/text()")[0]
                src = os.path.split(self._xpath(navPoint, "toc:content/@src")[0])[1]

                childTitles = addTitles(navPoint)
                titles.append((text, src, childTitles))

            return titles

        navMap = self._xpath(self._toc, "/toc:ncx/toc:navMap")[0]
        return addTitles(navMap)

    def _xpath(self, element, xpath):
        return element.xpath(xpath, namespaces={"toc": Toc._TOC_NS})