from lxml import etree


class OpfReader:
    OPF_NS = "http://www.idpf.org/2007/opf"
    DC_NS = "http://purl.org/dc/elements/1.1/"

    def __init__(self, opfContent):
        """
        @param opfContent: un string con el contenido de content.opf.
        """
        self._opf = etree.XML(opfContent)

    def getSpineItems(self):
        return self._xpath(self._opf, "/opf:package/opf:spine/opf:itemref/@idref")

    def getAuthors(self):
        authorsList = []

        authors = self._xpath(self._opf, "/opf:package/opf:metadata/dc:creator[@opf:role = 'aut']")
        for author in authors:
            authorName = self._xpath(author, "text()")[0]
            authorFileAs = self._xpath(author, "@opf:file-as")[0]
            authorsList.append((authorName, authorFileAs))

        return authorsList

    def getTranslators(self):
        translatorsList = []

        translators = self._xpath(self._opf, "/opf:package/opf:metadata/dc:contributor[@opf:role = 'trl']")
        for translator in translators:
            translatorName = self._xpath(translator, "text()")[0]
            translatorFileAs = self._xpath(translator, "@opf:file-as")[0]
            translatorsList.append((translatorName, translatorFileAs))

        return translatorsList

    def getIlustrators(self):
        ilustratorsList = []

        ilustrators = self._xpath(self._opf, "/opf:package/opf:metadata/dc:contributor[@opf:role = 'ill']")
        for ilustrator in ilustrators:
            ilustratorName = self._xpath(ilustrator, "text()")[0]
            ilustratorFileAs = self._xpath(ilustrator, "@opf:file-as")[0]
            ilustratorsList.append((ilustratorName, ilustratorFileAs))

        return ilustratorsList

    def getCalibreSerie(self):
        serieName = ""
        serieIndex = ""

        calibreSerie = self._xpath(self._opf, "/opf:package/opf:metadata/opf:meta[@name = 'calibre:series']")
        if len(calibreSerie) != 0:
            serieName = self._xpath(calibreSerie[0], "@content")[0]

        calibreSerieIndex = self._xpath(self._opf, "/opf:package/opf:metadata/opf:meta[@name = 'calibre:series_index']")
        if len(calibreSerieIndex) != 0:
            serieIndex = self._xpath(calibreSerieIndex[0], "@content")[0]

        return serieName, serieIndex

    def _xpath(self, element, xpath):
        return element.xpath(xpath, namespaces={"opf": OpfReader.OPF_NS, "dc": OpfReader.DC_NS})

