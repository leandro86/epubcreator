from lxml import etree


class Opf:
    _OPF_NS = "http://www.idpf.org/2007/opf"
    _DC_NS = "http://purl.org/dc/elements/1.1/"

    def __init__(self):
        self.metadata = Metadata()
        self.manifest = Manifest()
        self.spine = Spine()
        self.guide = Guide()

    def toXml(self):
        return etree.tostring(self._generateOpf(), encoding="utf-8", xml_declaration=True, pretty_print=True)

    def _generateOpf(self):
        opf = etree.Element("{{{0}}}package".format(Opf._OPF_NS), {"unique-identifier": "BookId", "version": "2.0"}, nsmap={None: Opf._OPF_NS})

        opf.append(self.metadata.toElement())
        opf.append(self.manifest.toElement())
        opf.append(self.spine.toElement())
        opf.append(self.guide.toElement())

        return opf


class Manifest:
    def __init__(self):
        self._items = []
        self._items.append(_ManifestItem("toc.ncx", "ncx"))

    def addItem(self, href, itemId):
        self._items.append(_ManifestItem(href, itemId))

    def toElement(self):
        manifest = etree.Element("manifest")

        for item in self._items:
            manifest.append(item.toElement())

        return manifest


class Spine:
    def __init__(self):
        self._idsRef = []

    def addItemRef(self, idRef):
        self._idsRef.append(idRef)

    def toElement(self):
        spine = etree.Element("spine", {"toc": "ncx"})

        for idRef in self._idsRef:
            etree.SubElement(spine, "itemref", {"idref": idRef})

        return spine


class Metadata:
    def __init__(self):
        self._dcItems = []
        self._items = []

    def addTitle(self, title):
        item = _MetadataDCItem("title", title)
        self._dcItems.append(item)

    def addLanguage(self, language):
        item = _MetadataDCItem("language", language)
        self._dcItems.append(item)

    def addIdentifier(self, identifier):
        item = _MetadataDCItem("identifier", identifier)
        item.addOpfAttribute("scheme", "UUID")
        item.addAttribute("id", "BookId")
        self._dcItems.append(item)

    def addModificationDate(self, date):
        item = _MetadataDCItem("date", date)
        item.addOpfAttribute("event", "modification")
        self._dcItems.append(item)

    def addPublisher(self, publisher):
        item = _MetadataDCItem("publisher", publisher)
        self._dcItems.append(item)

    def addPublicationDate(self, publicationDate):
        item = _MetadataDCItem("date", publicationDate.strftime("%Y-%m-%d"))
        item.addOpfAttribute("event", "publication")
        self._dcItems.append(item)

    def addDescription(self, description):
        item = _MetadataDCItem("description", description)
        self._dcItems.append(item)

    def addTranslator(self, translator, fileAs=""):
        item = _MetadataDCItem("contributor", translator)
        item.addOpfAttribute("role", "trl")
        item.addOpfAttribute("file-as", fileAs if fileAs else translator)
        self._dcItems.append(item)

    def addAuthor(self, author, fileAs=""):
        item = _MetadataDCItem("creator", author)
        item.addOpfAttribute("role", "aut")
        item.addOpfAttribute("file-as", fileAs if fileAs else author)
        self._dcItems.append(item)

    def addSubject(self, subject):
        item = _MetadataDCItem("subject", subject)
        self._dcItems.append(item)

    def addIlustrator(self, ilustrator, fileAs=""):
        item = _MetadataDCItem("contributor", ilustrator)
        item.addOpfAttribute("role", "ill")
        item.addOpfAttribute("file-as", fileAs if fileAs else ilustrator)
        self._dcItems.append(item)

    def addCustom(self, name, content):
        item = _MetadataItem(name, content)
        self._items.append(item)

    def toElement(self):
        metadata = etree.Element("metadata", nsmap={"opf": Opf._OPF_NS, "dc": Opf._DC_NS})

        for dcItem in self._dcItems:
            metadata.append(dcItem.toElement())

        for item in self._items:
            metadata.append(item.toElement())

        return metadata


class Guide:
    def __init__(self):
        self._guide = etree.Element("guide")

    def addReference(self, href, title, type):
        etree.SubElement(self._guide, "reference", {"href": href, "title": title, "type": type})

    def toElement(self):
        return self._guide


class _ManifestItem:
    _mediaTypes = {"ncx": "application/x-dtbncx+xml",
                   "xhtml": "application/xhtml+xml",
                   "css": "text/css",
                   "jpg": "image/jpeg",
                   "jpeg": "image/jpeg",
                   "png": "image/png",
                   "gif": "image/gif"}

    def __init__(self, href, itemId):
        self._href = href
        self._itemId = itemId
        self._mediaType = self._getMediaType(href)

    def toElement(self):
        return etree.Element("item", {"href": self._href, "id": self._itemId, "media-type": self._mediaType})

    def _getMediaType(self, href):
        ext = href[href.rfind(".") + 1:]
        return _ManifestItem._mediaTypes[ext]


class _MetadataDCItem:
    def __init__(self, name, content):
        self._name = name
        self._content = content
        self._attributes = {}
        self._opfAttributes = {}

    def addAttribute(self, name, value):
        self._attributes[name] = value

    def addOpfAttribute(self, name, value):
        self._opfAttributes[name] = value

    def toElement(self):
        dc_ns = "{{{0}}}".format(Opf._DC_NS)
        opf_ns = "{{{0}}}".format(Opf._OPF_NS)

        element = etree.Element(dc_ns + self._name)

        for name, value in self._attributes.items():
            element.set(name, value)

        for name, value in self._opfAttributes.items():
            element.set(opf_ns + name, value)

        element.text = self._content
        return element


class _MetadataItem:
    def __init__(self, name, content):
        self._name = name
        self._content = content

    def toElement(self):
        return etree.Element("meta", {"name": self._name, "content": self._content})