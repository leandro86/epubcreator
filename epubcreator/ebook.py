import os
import datetime
import re

import mako.template
from pyepub.pyepubwriter import epub

from epubcreator import ebook_metadata, ebook_data, epubbase_names
from misc import utils
import config


class _EpubBase:
    _files = {}

    def __init__(self, epubBaseFilesDirPath):
        if not _EpubBase._files:
            _EpubBase._loadEpubBaseFiles(epubBaseFilesDirPath)

    def getCover(self):
        return _EpubBase._files[epubbase_names.COVER_FILENAME]

    def getSynopsis(self, synopsis):
        template = _EpubBase._files[epubbase_names.SYNOPSIS_FILENAME]
        return template.render(synopsis=synopsis)

    def getTitle(self, author, title, subtitle, editor):
        template = _EpubBase._files[epubbase_names.TITLE_FILENAME]
        return template.render(author=author, title=title, subtitle=subtitle, editor=editor)

    def getInfo(self, originalTitle, author, publicationYear, translator, ilustrator, coverDesigner, coverDesignOrTweak,
                editor):
        template = _EpubBase._files[epubbase_names.INFO_FILENAME]
        return template.render(originalTitle=originalTitle, author=author, publicationYear=publicationYear,
                               translator=translator, ilustrator=ilustrator, coverDesigner=coverDesigner,
                               coverDesignOrTweak=coverDesignOrTweak, editor=editor)

    def getDedication(self, dedication):
        template = _EpubBase._files[epubbase_names.DEDICATION_FILENAME]
        return template.render(dedication=dedication)

    def getAuthor(self, authorBiography):
        template = _EpubBase._files[epubbase_names.AUTHOR_FILENAME]
        return template.render(authorBiography=authorBiography)

    def getEplLogoImage(self):
        return _EpubBase._files[epubbase_names.EPL_LOGO_FILENAME]

    def getExLibrisImage(self):
        return _EpubBase._files[epubbase_names.EX_LIBRIS_FILENAME]

    def getCss(self):
        return _EpubBase._files[epubbase_names.STYLE_FILENAME]

    def getCoverImage(self):
        return _EpubBase._files[epubbase_names.COVER_IMAGE_FILENAME]

    def getAuthorImage(self):
        return _EpubBase._files[epubbase_names.AUTHOR_IMAGE_FILENAME]

    def getIBooksEmbeddedFontsFile(self):
        return _EpubBase._files[epubbase_names.IBOOKS_EMBEDDED_FONTS_FILENAME]

    @staticmethod
    def _loadEpubBaseFiles(epubBaseFilesDirPath):
        fileNames = (epubbase_names.AUTHOR_FILENAME,
                     epubbase_names.AUTHOR_IMAGE_FILENAME,
                     epubbase_names.COVER_IMAGE_FILENAME,
                     epubbase_names.COVER_FILENAME,
                     epubbase_names.DEDICATION_FILENAME,
                     epubbase_names.EPL_LOGO_FILENAME,
                     epubbase_names.EX_LIBRIS_FILENAME,
                     epubbase_names.INFO_FILENAME,
                     epubbase_names.STYLE_FILENAME,
                     epubbase_names.SYNOPSIS_FILENAME,
                     epubbase_names.TITLE_FILENAME,
                     epubbase_names.IBOOKS_EMBEDDED_FONTS_FILENAME)

        for fileName in fileNames:
            filePath = os.path.join(epubBaseFilesDirPath, fileName)

            # Estos archivos son de texto común, y no necesito hacer nada especial
            # para abrirlos.
            textFiles = (epubbase_names.COVER_FILENAME,
                         epubbase_names.STYLE_FILENAME,
                         epubbase_names.IBOOKS_EMBEDDED_FONTS_FILENAME)

            if fileName.endswith(".png") or fileName.endswith(".jpg"):
                with open(filePath, "rb") as file:
                    _EpubBase._files[fileName] = file.read()
            elif fileName in textFiles:
                with open(filePath, encoding="utf-8") as file:
                    _EpubBase._files[fileName] = file.read()
            else:
                newFilePath = filePath.replace(".xhtml", ".mako")
                _EpubBase._files[fileName] = mako.template.Template(filename=newFilePath,
                                                                    input_encoding="utf-8",
                                                                    output_encoding="utf-8")


class Ebook:
    _epubBase = _EpubBase(config.EPUBBASE_FILES_DIR_PATH)

    def __init__(self, ebookData, metadata=None):
        self._ebookData = ebookData or ebook_data.EbookData()
        self._metadata = metadata or ebook_metadata.Metadata()
        self._hasEbookNotes = self._ebookData.sections and type(self._ebookData.sections[-1]) == ebook_data.NotesSection

        # Hay algunos datos que indefectiblemente deben estar en el epub, por más
        # que el usuario no los haya especificado.
        self._setDefaultMetadata()

    def save(self, file):
        """
        Genera y guarda el epub.
        
        @param file: un string con el directorio donde guardar el epub (no el nombre del
                     archivo, ya que este debe generarse de acuerdo a los metadatos), o un objeto file-like.

        @return: el path del archivo generado, si "file" es un string. Si "file" es un objeto de tipo
                 file-like, se retorna el nombre de archivo del epub.
        """
        outputEpub = epub.EpubWriter()

        self._addEpubBaseFiles(outputEpub)
        self._addSections(outputEpub)
        self._addImages(outputEpub)
        self._addMetadata(outputEpub)
        self._setupToc(outputEpub)

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
        publicationYear = ""
        if type(self._metadata.publicationDate) is datetime.date:
            publicationYear = str(self._metadata.publicationDate.year)

        authors = self._formatPersons(self._metadata.authors)[0]
        translators = self._formatPersons(self._metadata.translators)[0]
        ilustrators = self._formatPersons(self._metadata.ilustrators)[0]

        # Agrego los xhtml requeridos
        outputEpub.addHtmlData(epubbase_names.COVER_FILENAME, Ebook._epubBase.getCover())
        outputEpub.addHtmlData(epubbase_names.SYNOPSIS_FILENAME, Ebook._epubBase.getSynopsis(self._metadata.synopsis))
        outputEpub.addHtmlData(epubbase_names.TITLE_FILENAME, Ebook._epubBase.getTitle(authors,
                                                                                       self._metadata.title,
                                                                                       self._metadata.subtitle,
                                                                                       self._metadata.editor))
        outputEpub.addHtmlData(epubbase_names.INFO_FILENAME, Ebook._epubBase.getInfo(self._metadata.originalTitle,
                                                                                     authors,
                                                                                     publicationYear,
                                                                                     translators,
                                                                                     ilustrators,
                                                                                     self._metadata.coverDesigner,
                                                                                     self._metadata.coverDesignOrTweak,
                                                                                     self._metadata.editor))
        outputEpub.addHtmlData(epubbase_names.DEDICATION_FILENAME,
                               Ebook._epubBase.getDedication(self._metadata.dedication))

        # Cargo la cover por defecto si el usuario no especificó una
        if self._metadata.coverImage is None:
            self._metadata.coverImage = Ebook._epubBase.getCoverImage()

        outputEpub.addImageData(epubbase_names.COVER_IMAGE_FILENAME, self._metadata.coverImage)

        # Cargo la imagen de autor por defecto si el usuario no especificó una
        if self._metadata.authorImage is None:
            self._metadata.authorImage = Ebook._epubBase.getAuthorImage()

        outputEpub.addImageData(epubbase_names.AUTHOR_IMAGE_FILENAME, self._metadata.authorImage)

        # Agrego el resto de los archivos del epubbase
        outputEpub.addImageData(epubbase_names.EPL_LOGO_FILENAME, Ebook._epubBase.getEplLogoImage())
        outputEpub.addImageData(epubbase_names.EX_LIBRIS_FILENAME, Ebook._epubBase.getExLibrisImage())
        outputEpub.addStyleData(epubbase_names.STYLE_FILENAME, Ebook._epubBase.getCss())
        outputEpub.addMetaFile(epubbase_names.IBOOKS_EMBEDDED_FONTS_FILENAME,
                               Ebook._epubBase.getIBooksEmbeddedFontsFile())

    def _addSections(self, outputEpub):
        for section in self._ebookData.sections[:-1] if self._hasEbookNotes else self._ebookData.sections:
            outputEpub.addHtmlData(section.name, section.toHtml())

        authorContent = Ebook._epubBase.getAuthor(self._metadata.authorBiography)

        if self._hasEbookNotes:
            notesSection = self._ebookData.sections[-1]
            outputEpub.addHtmlData(epubbase_names.AUTHOR_FILENAME, authorContent)
            outputEpub.addHtmlData(notesSection.name, notesSection.toHtml())
        else:
            outputEpub.addHtmlData(epubbase_names.AUTHOR_FILENAME, authorContent)

    def _addImages(self, outputEpub):
        for image in self._ebookData.images:
            outputEpub.addImageData(image.name, image.content)

    def _addMetadata(self, outputEpub):
        if not self._metadata.publisher:
            self._metadata.publisher = "ePubLibre"

        # Ordeno los géneros alfabéticamente...
        self._metadata.genres.sort(key=lambda x: (x.genreType, x.genre, x.subGenre))

        genres = []
        previousGenre = ""
        for genre in self._metadata.genres:
            if genre.genre != previousGenre:
                genres.append(genre.genre)
                previousGenre = genre.genre
            genres.append(genre.subGenre)

        authors = self._formatPersons(self._metadata.authors)

        # Agrego semántica a cubierta.xhtml
        outputEpub.addReference(epubbase_names.COVER_FILENAME, "Cover", "cover")

        # Es necesario agregarle semántica a cover.jpg, sino algunos ereaders no la reconocen como imagen de portada
        outputEpub.addCustomMetadata("cover", epubbase_names.COVER_IMAGE_FILENAME)

        outputEpub.addTitle(self._metadata.title)
        outputEpub.addAuthor(authors[0], authors[1])
        outputEpub.addLanguage(self._metadata.language)
        outputEpub.addDescription(self._purgeStringForMetadata(self._metadata.synopsis))
        outputEpub.addPublisher(self._metadata.publisher)
        outputEpub.addSubject(", ".join(genres))

        if self._metadata.translators:
            translators = self._formatPersons(self._metadata.translators)
            outputEpub.addTranslator(translators[0], translators[1])

        if self._metadata.ilustrators:
            ilustrators = self._formatPersons(self._metadata.ilustrators)
            outputEpub.addIlustrator(ilustrators[0], ilustrators[1])

        if self._metadata.publicationDate is not None:
            outputEpub.addPublicationDate(self._metadata.publicationDate)

        if self._metadata.subCollectionName:
            calibreSeries = ""

            if self._metadata.collectionName:
                calibreSeries += "{0}: ".format(self._metadata.collectionName)
            calibreSeries += self._metadata.subCollectionName

            try:
                # Elimino los ceros a la izquierda si se trata de un número
                series_index = str(int(self._metadata.collectionVolume))
            except ValueError:
                series_index = self._metadata.collectionVolume

            outputEpub.addCustomMetadata("calibre:series", calibreSeries)
            outputEpub.addCustomMetadata("calibre:series_index", series_index)

    def _setupToc(self, outputEpub):
        """
        Crea la tabla de contenidos del epub.
        
        @param outputEpub: el epub donde está la toc.
        """
        # La cubierta debe ser la primera entrada en la toc
        outputEpub.addNavPoint(epubbase_names.COVER_FILENAME, "Cubierta")

        # El título del libro debe ser la segunda entrada en la toc
        outputEpub.addNavPoint(epubbase_names.TITLE_FILENAME, self._metadata.title)

        self._ebookData.toc.addFirstLevelTitle(epubbase_names.AUTHOR_FILENAME, "Autor", False)

        if self._hasEbookNotes:
            self._ebookData.toc.addFirstLevelTitle(epubbase_names.NOTES_FILENAME, "Notas", False)

        def addTitlesToToc(navPoint, titles):
            for childTitle in titles:
                childNavPoint = navPoint.addNavPoint(childTitle.titleLocation, childTitle.text)
                addTitlesToToc(childNavPoint, childTitle.childTitles)

        for title in self._ebookData.toc.titles:
            rootNavPoint = outputEpub.addNavPoint(title.titleLocation, title.text)
            addTitlesToToc(rootNavPoint, title.childTitles)

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

    def _purgeStringForMetadata(self, s):
        """
        Elimina tags de un string y convierte los saltos de línea por un espacio, de
        manera tal de que sea válido para agregarlo a los metadatos del epub.

        @param s: el string a convertir.

        @return: el string convertido.
        """
        return re.sub("<[^>]*>", "", s.replace("\n", " "))

    def _setDefaultMetadata(self):
        if not self._metadata.synopsis:
            self._metadata.synopsis = ebook_metadata.Metadata.DEFAULT_SYNOPSIS

        if not self._metadata.title:
            self._metadata.title = ebook_metadata.Metadata.DEFAULT_TITLE

        if not self._metadata.authors:
            self._metadata.addAuthor(ebook_metadata.Metadata.DEFAULT_AUTHOR, ebook_metadata.Metadata.DEFAULT_AUTHOR)

        if not self._metadata.editor:
            self._metadata.editor = ebook_metadata.Metadata.DEFAULT_EDITOR

        if not self._metadata.language:
            self._metadata.language = ebook_metadata.Metadata.DEFAULT_LANGUAGE

        if not self._metadata.coverDesignOrTweak:
            self._metadata.coverDesignOrTweak = "Diseño"

        if not self._metadata.coverDesigner:
            self._metadata.coverDesigner = ebook_metadata.Metadata.DEFAULT_EDITOR

        if not self._metadata.dedication:
            self._metadata.dedication = ebook_metadata.Metadata.DEFAULT_DEDICATION

        if not self._metadata.authorBiography:
            self._metadata.authorBiography = ebook_metadata.Metadata.DEFAULT_AUTHOR_BIOGRAPHY