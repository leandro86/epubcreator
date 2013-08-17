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

import os
import datetime

from lxml import etree
from pyepub.pyepubwriter import epub

from ecreator import ebook_data
from misc import utils
import config


class Ebook:

    COVER_EP_NAME = "cubierta.xhtml"
    SYNOPSIS_EP_NAME = "sinopsis.xhtml"
    TITLE_EP_NAME = "titulo.xhtml"
    INFO_EP_NAME = "info.xhtml"
    DEDICATION_EP_NAME = "dedicatoria.xhtml"
    AUTHOR_EP_NAME = "autor.xhtml"
    NOTES_EP_NAME = "notas.xhtml"
    COVER_IMAGE_EP_NAME = "cover.jpg"
    AUTHOR_IMAGE_EP_NAME = "autor.jpg"

    def __init__(self, files = None, titles = None, metadata = None):
        self._files = files or []
        self._titles = titles or []
        self._metadata = metadata or ebook_data.Metadata()

    def save(self, file):
        """
        Genera y guarda el epub.
        
        @param file: un string con el directorio donde guardar el epub (no el nombre del
                     archivo, ya que este debe generarse de acuerdo a los metadatos), o un objeto file-like.

        @raise: IOError, si el ebook no pudo guardarse.

        @return: el path del archivo generado, si "file" es un string. Si "file" es un objeto de tipo
                 file-like, se retorna el nombre de archivo del epub.
        """
        outputEpub = epub.Epub()

        self._addEpubBaseFiles(outputEpub)
        self._addTextSections(outputEpub)
        self._addImages(outputEpub)
        self._setupToc(outputEpub)
        self._addMetadata(outputEpub)

        epubName = self._getOutputFileName()

        # Compruebo si estoy ante un string (o sea, un directorio) o un objeto file-like
        if isinstance(file, str):
            fileName = os.path.join(file, epubName)
            outputEpub.generate(fileName)
            return fileName
        else:
            outputEpub.generate(file)
            return epubName

    def _addEpubBaseFiles(self, outputEpub):
        templates = _EpubBaseTemplate(config.EPUBBASE_FILES_DIR_PATH)

        publicationYear = ""
        if type(self._metadata.publicationDate) is datetime.date:
            publicationYear = str(self._metadata.publicationDate.year)

        authors = self._formatPersons(self._metadata.authors)[0]
        translators = self._formatPersons(self._metadata.translators)[0]
        ilustrators = self._formatPersons(self._metadata.ilustrators)[0]

        # Agrego los xhtml requeridos
        outputEpub.addHtmlData(Ebook.COVER_EP_NAME, templates.getCover())
        outputEpub.addHtmlData(Ebook.SYNOPSIS_EP_NAME, templates.getSynopsis(self._metadata.synopsis))
        outputEpub.addHtmlData(Ebook.TITLE_EP_NAME, templates.getTitle(authors,
                                                                       self._metadata.title,
                                                                       self._metadata.subtitle,
                                                                       self._metadata.editor))
        outputEpub.addHtmlData(Ebook.INFO_EP_NAME, templates.getInfo(self._metadata.originalTitle,
                                                                     authors,
                                                                     publicationYear,
                                                                     translators,
                                                                     ilustrators,
                                                                     self._metadata.coverDesigner,
                                                                     self._metadata.coverDesignOrTweak,
                                                                     self._metadata.editor))
        outputEpub.addHtmlData(Ebook.DEDICATION_EP_NAME, templates.getDedication(self._metadata.dedication))

        # El epubbase indica que el autor.xhtml debe ser la última sección del epub. No puedo agregarlo al epub
        # directamente acá, porque luego inserto las secciones propiamente dichas, y me quedaría el autor.xhtml antes
        # de las secciones. Dado que en esta lista ya tengo todos los archivos agregados por el usuario, simplemente
        # agrego el autor.xhtml al final de la misma.
        # Además, si el ebook tiene una sección de notas, entonces el autor.xhtml ya no va al final, sino que debe
        # ir justo antes de las notas(que invariablemente siempre va a ser el último archivo)
        pos = len(self._files)
        if self._files and self._files[-1].name == Ebook.NOTES_EP_NAME:
            pos = len(self._files) - 1
        self._files.insert(pos, ebook_data.File(Ebook.AUTHOR_EP_NAME, ebook_data.File.FILE_TYPE.TEXT,
                                                templates.getAuthor(self._metadata.authorBiography)))

        coverImagePath = os.path.join(config.EPUBBASE_FILES_DIR_PATH, Ebook.COVER_IMAGE_EP_NAME)
        authorImagePath = os.path.join(config.EPUBBASE_FILES_DIR_PATH, Ebook.AUTHOR_IMAGE_EP_NAME)
        logoPath = os.path.join(config.EPUBBASE_FILES_DIR_PATH, "EPL_logo.png")
        exLibrisPath = os.path.join(config.EPUBBASE_FILES_DIR_PATH, "ex_libris.png")
        styleCssPath = os.path.join(config.EPUBBASE_FILES_DIR_PATH, "style.css")

        # Cargo la cover por defecto si el usuario no especificó una
        coverImageData = self._metadata.coverImage
        if self._metadata.coverImage is None:
            with open(coverImagePath, "rb") as coverImage:
                coverImageData = coverImage.read()

        # Cargo la imagen de autor por defecto si el usuario no especificó una
        authorImageData = self._metadata.authorImage
        if self._metadata.authorImage is None:
            with open(authorImagePath, "rb") as authorImage:
                authorImageData = authorImage.read()

        # Agrego la cover y el resto imágenes y css requeridos
        outputEpub.addImageData(Ebook.COVER_IMAGE_EP_NAME, coverImageData)
        outputEpub.addImageData(Ebook.AUTHOR_IMAGE_EP_NAME, authorImageData)

        with open(logoPath, "rb") as logo, open(exLibrisPath, "rb") as exLibris, open(styleCssPath, encoding="utf-8") as styleCss:
            outputEpub.addImageData("EPL_logo.png", logo.read())
            outputEpub.addImageData("ex_libris.png", exLibris.read())
            outputEpub.addStyleData("style.css", styleCss.read())

    def _addTextSections(self, outputEpub):
        """
        Agrega las secciones al epub.
        
        @param outputEpub: el epub donde van a agregarse las secciones.
        """
        textFiles = [file for file in self._files if file.fileType == ebook_data.File.FILE_TYPE.TEXT]
        for textFile in textFiles:
            outputEpub.addHtmlData(textFile.name, textFile.content)

    def _addImages(self, outputEpub):
        imageFiles = [file for file in self._files if file.fileType == ebook_data.File.FILE_TYPE.IMAGE]
        for imageFile in imageFiles:
            outputEpub.addImageData(imageFile.name, imageFile.content)

    def _addMetadata(self, outputEpub):
        # Me aseguro de tener algunos metadatos por defecto, en caso de que estén vacíos...
        if not self._metadata.title:
            self._metadata.title = "Título"

        if not self._metadata.authors:
            self._metadata.authors.append(ebook_data.Person("Nombre Apellido", "Apellido, Nombre"))

        if not self._metadata.language:
            self._metadata.language = "es"

        if not self._metadata.genres:
            self._metadata.genres.append(ebook_data.Genre("Bla", "Género", "Subgéneros"))

        if not self._metadata.synopsis:
            self._metadata.synopsis = "Sinopsis"

        if not self._metadata.publisher:
            self._metadata.publisher = "ePubLibre"

        # Ordeno los géneros alfabéticamente...
        self._metadata.genres.sort(key = lambda x: (x.genreType, x.genre, x.subGenre))

        genres = []
        previousGenre = ""
        for genre in self._metadata.genres:
            if genre.genre != previousGenre:
                genres.append(genre.genre)
                previousGenre = genre.genre
            genres.append(genre.subGenre)

        authors = self._formatPersons(self._metadata.authors)

        # Agrego semántica a cubierta.xhtml
        outputEpub.addReference("cubierta.xhtml", "Cover", "cover")

        # Es necesario agregarle semántica a cover.jpg, sino algunos ereaders no la reconocen como imagen de portada
        outputEpub.addCustomMetadata("cover", Ebook.COVER_IMAGE_EP_NAME)

        outputEpub.addTitle(self._metadata.title)
        outputEpub.addAuthor(authors[0], authors[1])
        outputEpub.addLanguage(self._metadata.language)
        outputEpub.addDescription(self._metadata.synopsis)
        outputEpub.addPublisher(self._metadata.publisher)
        outputEpub.addSubject(", ".join(genres))

        for translator in self._metadata.translators:
            outputEpub.addTranslator(translator.name, translator.fileAs)

        for ilustrator in self._metadata.ilustrators:
            outputEpub.addIlustrator(ilustrator.name, ilustrator.fileAs)

        if self._metadata.publicationDate is not None:
            outputEpub.addPublicationDate(self._metadata.publicationDate)

        if self._metadata.subCollectionName:
            calibreSeries = ""

            if self._metadata.collectionName:
                calibreSeries += "{0}: ".format(self._metadata.collectionName)
            calibreSeries += self._metadata.subCollectionName

            outputEpub.addCustomMetadata("calibre:series", calibreSeries)
            outputEpub.addCustomMetadata("calibre:series_index", self._metadata.collectionVolume)

    def _setupToc(self, outputEpub):
        """
        Crea la tabla de contenidos del epub.
        
        @param outputEpub: el epub donde está la toc.
        """        
        # La cubierta debe ser el primer título en la toc
        outputEpub.addNavPoint(Ebook.COVER_EP_NAME, "Cubierta")
        
        for title in self._titles:
            rootNavPoint = outputEpub.addNavPoint(title.titleLocation, title.text)
            self._addTitlesToToc(rootNavPoint, title.childTitles)

    def _addTitlesToToc(self, navPoint, titles):
        """
        Agrega los títulos de manera recursiva a la toc.
        
        @param navPoint: un objeto NavPoint.
        @param titles: una lista de Title.
        """
        for childTitle in titles:
            childNavPoint = navPoint.addNavPoint(childTitle.titleLocation, childTitle.text)
            self._addTitlesToToc(childNavPoint, childTitle.childTitles)

    def _getOutputFileName(self):
        fileName = []
        authorsFileAs = [author.fileAs for author in self._metadata.authors]
        if len(authorsFileAs) < 3:
            fileName.append(" & ".join(authorsFileAs))
        else:
            fileName.append("AA. VV.")

        fileName.append(" - ")

        if self._metadata.subCollectionName:
            collection = ""

            if self._metadata.collectionName:
                collection += "[{0}] ".format(self._metadata.collectionName)
            collection += "[{0} {1}] ".format(self._metadata.subCollectionName, self._metadata.collectionVolume)

            if self._metadata.collectionName:
                fileName.insert(0, collection)
            else:
                fileName.append(collection)

        fileName.append(self._metadata.title)
        fileName.append(" (r1.0 {0})".format(self._metadata.editor if self._metadata.editor else "El Editor"))

        return utils.Utilities.purgeString("{0}.epub".format("".join(fileName)))

    def _formatPersons(self, personsList):
        """
        Formatea una lista de Person de manera acorde según el epubbase para ser insertada en el epub.

        @param personsList: una lista de Person.

        @return: una tupla cuyo primer elemento es un string concatenado con todos los nombres, y el
                 segundo un string concatenado con todos los file-as.
        """
        return " & ".join([p.name for p in personsList]), " & ".join([p.fileAs for p in personsList])


class _EpubBaseTemplate:

    def __init__(self, epubBaseTemplatesPath):
        self._templatesPath = epubBaseTemplatesPath

    def getCover(self):
        return self._getTemplate("cover.xslt")

    def getSynopsis(self, synopsis):
        # En este método, como en los restantes, en lugar de ir agregando los parámetros a un diccionario uno
        # por uno, utilizo "locals()" para obtener todas las variables locales. Me valgo del hecho de que he
        # nombrado los parámetros de cada uno de los métodos, de igual manera a como están nombrados en la
        # planilla de transformación que crea el archivo base correspondiente. Es decir, en este caso, el
        # parámetro "synopsis" se llama de igual manera dentro de la planilla "sinopsis.xslt".
        params = locals()
        del(params["self"])
        self._prepareParams(params)

        return self._getTemplate("synopsis.xslt", params)

    def getTitle(self, author, title, subtitle, editor):
        params = locals()
        del(params["self"])
        self._prepareParams(params)

        return self._getTemplate("title.xslt", params)

    def getInfo(self, originalTitle, author, publicationYear, translator, ilustrator, coverDesigner,
                coverDesignOrTweak, editor):
        params = locals()
        del(params["self"])
        self._prepareParams(params)

        return self._getTemplate("info.xslt", params)

    def getDedication(self, dedication):
        params = locals()
        del(params["self"])
        self._prepareParams(params)

        return self._getTemplate("dedication.xslt", params)

    def getAuthor(self, authorBiography):
        params = locals()
        del(params["self"])
        self._prepareParams(params)

        return self._getTemplate("author.xslt", params)

    def _prepareParams(self, params):
        # Es necesario llamar a este método antes de enviarle los parámetros de transformación a la planilla.
        # Es el encargado de formatear el diccionario de parámetros de manera acorde.
        # Elimina parámetros con valores nulos o con un string vacío, ya que supongo entonces que dichos campos deben
        # ser eliminados del archivo del epubbase correspondiente. Ahora, si realmente van a ser eliminados o no
        # depende de la planilla, ya que ciertos campos son obligatorios, en cuyo caso, en lugar de eliminar un
        # campo se va a colocar el valor por defecto.
        # También, a través de "strparam", se hace un "escape" de comillas simples, dobles, etc.
        for key, value in list(params.items()):
            if value:
                params[key] = etree.XSLT.strparam(value)
            else:
                del(params[key])

    def _getTemplate(self, templateFileName, params = None):
        """
        Retorna el template del epubbase construido de acuerdo a los parámetros pasados.

        @param templateFileName: el nombre de la planilla xslt que construye el template.
        @param params: un diccionario con los parámetros a pasarle a la planilla.

        @return: un string con el contenido del archivo del epubbase resultante.
        """
        if not params:
            params = {}

        stylesheet = self._openStylesheet(os.path.join(self._templatesPath, templateFileName))
        transformer = etree.XSLT(stylesheet)

        return str(transformer(stylesheet, **params))
        #return etree.tostring(transformer(stylesheet, **params), xml_declaration = True, encoding = "utf-8")

    def _openStylesheet(self, pathToStylesheet):
        with open(pathToStylesheet, encoding="utf-8") as file:
            return etree.XML(file.read().encode("utf-8"))