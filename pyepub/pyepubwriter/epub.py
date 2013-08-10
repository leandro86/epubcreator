# -*- coding: utf-8 -*-

# Copyright (C) 2013 Leandro
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import zipfile
import uuid
import datetime

from lxml import etree

from pyepub.pyepubwriter import opf, toc


class Epub:
    
    def __init__(self):
        self._opf = opf.Opf()
        self._toc = toc.Toc()

        # Contiene todos los archivos agregados por el usuario al epub.
        # La key representa el path completo donde guardar el archivo dentro del epub, y el value es el contenido
        # del archivo, en string o bytes.
        self._files = {}
    
    def addHtmlData(self, name, content):           
        """
        Agrega un html al epub.
        
        @param name: el nombre con el que se va a guardar el html en el epub.
        @param content: el contenido del html. Puede ser un string o bytes.
        """
        self._opf.manifest.addItem("Text/{0}".format(name), name)
        self._opf.spine.addItemRef(name)        
        self._files["OEBPS/Text/{0}".format(name)] = content
    
    def addImageData(self, name, content):
        """
        Agrega una imagen al epub.
        
        @param name: el nombre con el que se va a guardar la imagen en el epub.
        @param content: el contenido de la imagen, en bytes.
        """
        self._opf.manifest.addItem("Images/{0}".format(name), name)
        self._files["OEBPS/Images/{0}".format(name)] =  content
    
    def addStyleData(self, name, content):
        """
        Agrega un css al epub.
        
        @param name: el nombre con el que se va a guardar el css en el epub.
        @param content: el contenido del css. Puede ser un string o bytes.
        """                
        self._opf.manifest.addItem("Styles/{0}".format(name), name)
        self._files["OEBPS/Styles/{0}".format(name)] = content

    def addNavPoint(self, ref, title):
        """
        Agrega un navPoint de primer nivel a la toc.
        
        @param ref: el nombre de archivo xhtml al cual apunta el navPoint.
        @param title: el título del navPoint.

        @return: el navPoint agregado.
        """
        return self._toc.addNavPoint(ref, title)

    def addReference(self, fileName, title, type):
        self._opf.guide.addReference("Text/{0}".format(fileName), title, type)

    def addTitle(self, title):
        self._opf.metadata.addTitle(title)
        self._toc.addTitle(title)

    def addLanguage(self, language):
        self._opf.metadata.addLanguage(language)

    def addPublisher(self, publisher):
        self._opf.metadata.addPublisher(publisher)

    def addPublicationDate(self, publicationDate):
        self._opf.metadata.addPublicationDate(publicationDate)

    def addDescription(self, description):
        self._opf.metadata.addDescription(description)

    def addTranslator(self, translator, fileAs = ""):
        self._opf.metadata.addTranslator(translator, fileAs)

    def addAuthor(self, author, fileAs = ""):
        self._opf.metadata.addAuthor(author, fileAs)

    def addSubject(self, subject):
        self._opf.metadata.addSubject(subject)

    def addIlustrator(self, ilustrator, fileAs = ""):
        self._opf.metadata.addIlustrator(ilustrator, fileAs)

    def addCustomMetadata(self, name, content):
        self._opf.metadata.addCustom(name, content)
                                                                       
    def generate(self, outputFile):
        """
        Genera el epub.
        
        @param outputFile: el path del archivo a generar, o un objeto de tipo file.

        @raise: IOError, si el epub no pudo guardarse.
        """
        epubFile = zipfile.ZipFile(outputFile, "w")

        self._addIdentifier()
        self._opf.metadata.addModificationDate(datetime.datetime.now().strftime("%Y-%m-%d"))

        epubFile.writestr("mimetype", "application/epub+zip", zipfile.ZIP_STORED)
        epubFile.writestr("META-INF/container.xml", self._generateContainer(), compress_type = zipfile.ZIP_DEFLATED)
        epubFile.writestr("OEBPS/content.opf", self._opf.toXml(), compress_type = zipfile.ZIP_DEFLATED)
        epubFile.writestr("OEBPS/toc.ncx", self._toc.toXml(), compress_type = zipfile.ZIP_DEFLATED)                

        for filePath, fileContent in self._files.items():
            epubFile.writestr(filePath, fileContent, compress_type = zipfile.ZIP_DEFLATED)

        epubFile.close()
    
    def _addIdentifier(self):
        uid = "urn:uuid:{0}".format(str(uuid.uuid4()))
        self._opf.metadata.addIdentifier(uid)
        self._toc.addIdentifier(uid)
    
    def _generateContainer(self):
        """
        Genera el contenido de container.xml.

        @return: un string con el contenido de container.xml.
        """
        container = etree.Element("container",
                                  {"version": "1.0", "xmlns": "urn:oasis:names:tc:opendocument:xmlns:container"})
        rootFiles = etree.SubElement(container, "rootfiles")
        etree.SubElement(rootFiles, "rootfile",
                         {"full-path": "OEBPS/content.opf", "media-type": "application/oebps-package+xml"})

        return etree.tostring(container, encoding="UTF-8", xml_declaration=True, pretty_print=True)