import os
import zipfile

from lxml import etree

from epubcreator.converters.docx import utils


class Docx:
    _DOCUMENT = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
    _STYLES = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles"
    _FOOTNOTES = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/footnotes"

    def __init__(self, file):
        self._docx = zipfile.ZipFile(file)
        self._namelist = frozenset(self._docx.namelist())
        self._documentDir, self._documentName = os.path.split(self._readDocumentFullPath())
        self._documentRelsByType, self._documentRelsById = self._readDocumentRels()
        self._footnotesRelsById = self._readFootnotesRels()

    def document(self):
        return self._docx.open(self._documentDir + "/" + self._documentName)

    def styles(self):
        return self._docx.open(self._documentDir + "/" + self._documentRelsByType[Docx._STYLES]) if self.hasStyles() else None

    def footnotes(self):
        return self._docx.open(self._documentDir + "/" + self._documentRelsByType[Docx._FOOTNOTES]) if self.hasFootnotes() else None

    def hasFootnotes(self):
        return Docx._FOOTNOTES in self._documentRelsByType

    def documentTarget(self, idd):
        return self._documentDir + "/" + self._documentRelsById[idd]

    def footnotesTarget(self, idd):
        return self._documentDir + "/" + self._footnotesRelsById[idd]

    def hasStyles(self):
        return Docx._STYLES in self._documentRelsByType

    def read(self, name):
        return self._docx.read(name)

    def _readDocumentFullPath(self):
        rels = etree.parse(self._docx.open("_rels/.rels"))
        documentName = utils.xpath(rels.getroot(), "/rels:Relationships/rels:Relationship[@Type = '{0}']/@Target".format(Docx._DOCUMENT))

        if not documentName:
            raise InvalidDocx("No existe un document.xml")

        return documentName[0]

    def _readDocumentRels(self):
        relsName = self._documentDir + "/_rels/" + self._documentName + ".rels"
        documentRelsByType = {}
        documentRelsById = {}

        if relsName in self._namelist:
            rels = etree.parse(self._docx.open(relsName))

            for item in rels.getroot():
                typ = item.get("Type")
                target = item.get("Target")
                idd = item.get("Id")

                documentRelsByType[typ] = target
                documentRelsById[idd] = target

        return documentRelsByType, documentRelsById

    def _readFootnotesRels(self):
        footnotesRelsById = {}

        if self.hasFootnotes():
            relsName = self._documentDir + "/_rels/" + self._documentRelsByType[Docx._FOOTNOTES] + ".rels"

            if relsName in self._namelist:
                rels = etree.parse(self._docx.open(relsName))

                for item in rels.getroot():
                    target = item.get("Target")
                    idd = item.get("Id")

                    footnotesRelsById[idd] = target

        return footnotesRelsById


class InvalidDocx(Exception):
    pass