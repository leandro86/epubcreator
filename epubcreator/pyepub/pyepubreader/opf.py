from lxml import etree


class Opf:
    _OPF_NS = "http://www.idpf.org/2007/opf"
    DC_NS = "http://purl.org/dc/elements/1.1/"

    def __init__(self, opfContent):
        """
        @param opfContent: un string con el contenido de content.opf.
        """
        self._opf = etree.fromstring(opfContent)

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

    def getDescription(self):
        description = self._xpath(self._opf, "/opf:package/opf:metadata/dc:description/text()")
        return description[0] if description else None

    def getTitle(self):
        title = self._xpath(self._opf, "/opf:package/opf:metadata/dc:title/text()")
        return title[0] if title else None

    def getLanguage(self):
        language = self._xpath(self._opf, "/opf:package/opf:metadata/dc:language/text()")
        return language[0] if language else None

    def getModificationDate(self):
        modificationDate = self._xpath(self._opf, "/opf:package/opf:metadata/dc:date[@opf:event = 'modification']/text()")
        return modificationDate[0] if modificationDate else None

    def getPublicationDate(self):
        publicationDate = self._xpath(self._opf, "/opf:package/opf:metadata/dc:date[@opf:event = 'publication']/text()")
        return publicationDate[0] if publicationDate else None

    def getPublisher(self):
        publisher = self._xpath(self._opf, "/opf:package/opf:metadata/dc:publisher/text()")
        return publisher[0] if publisher else None

    def getSubject(self):
        subject = self._xpath(self._opf, "/opf:package/opf:metadata/dc:subject/text()")
        return subject[0] if subject else None

    def getPathToToc(self):
        return self._xpath(self._opf, "/opf:package/opf:manifest/opf:item[@media-type = 'application/x-dtbncx+xml']/@href")[0]

    def _xpath(self, element, xpath):
        return element.xpath(xpath, namespaces={"opf": Opf._OPF_NS, "dc": Opf.DC_NS})