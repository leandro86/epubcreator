import os
import copy

import mako.template
from epubcreator.pyepub.pyepubwriter import epub

from epubcreator.epubbase import ebook_metadata, ebook_data, epubbase_names
from epubcreator.epubbase.misc import utils
from epubcreator import config
from epubcreator.misc.options import Options, Option


class _Templates:
    _files = {}

    def __init__(self, epubBaseFilesDirPath):
        if not _Templates._files:
            _Templates._loadEpubBaseFiles(epubBaseFilesDirPath)

    def getCover(self):
        return _Templates._files[epubbase_names.COVER_FILENAME]

    def getSynopsis(self, synopsis):
        params = locals()
        del (params["self"])

        template = _Templates._files[epubbase_names.SYNOPSIS_FILENAME]
        return template.render(**params)

    def getTitle(self, author, title, subtitle, editor, collectionName, subCollectionName, collectionVolume):
        params = locals()
        del (params["self"])

        template = _Templates._files[epubbase_names.TITLE_FILENAME]
        return template.render(**params)

    def getInfo(self, originalTitle, author, publicationYear, translator, ilustrator, coverDesigner, coverModification, editor):
        params = locals()
        del (params["self"])

        template = _Templates._files[epubbase_names.INFO_FILENAME]
        return template.render(**params)

    def getDedication(self, dedication):
        params = locals()
        del (params["self"])

        template = _Templates._files[epubbase_names.DEDICATION_FILENAME]
        return template.render(**params)

    def getAuthor(self, authorBiography, title, imageName):
        params = locals()
        del (params["self"])

        template = _Templates._files[epubbase_names.AUTHOR_FILENAME]
        return template.render(**params)

    def getEplLogoImage(self):
        return _Templates._files[epubbase_names.EPL_LOGO_FILENAME]

    def getExLibrisImage(self):
        return _Templates._files[epubbase_names.EX_LIBRIS_FILENAME]

    def getCss(self):
        return _Templates._files[epubbase_names.STYLE_FILENAME]

    def getCoverImage(self):
        return _Templates._files[epubbase_names.COVER_IMAGE_FILENAME]

    def getAuthorImage(self):
        return _Templates._files[epubbase_names.AUTHOR_IMAGE_FILENAME]

    def getIBooksDisplayOptionsFile(self):
        return _Templates._files[epubbase_names.IBOOKS_DISPLAY_OPTIONS_FILE_NAME]

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
                     epubbase_names.IBOOKS_DISPLAY_OPTIONS_FILE_NAME)

        for fileName in fileNames:
            filePath = os.path.join(epubBaseFilesDirPath, fileName)

            # Estos archivos son de texto común, y no necesito hacer nada especial
            # para abrirlos.
            textFiles = (epubbase_names.COVER_FILENAME,
                         epubbase_names.STYLE_FILENAME,
                         epubbase_names.IBOOKS_DISPLAY_OPTIONS_FILE_NAME)

            if fileName.endswith(".png") or fileName.endswith(".jpg"):
                with open(filePath, "rb") as file:
                    _Templates._files[fileName] = file.read()
            elif fileName in textFiles:
                with open(filePath, encoding="utf-8") as file:
                    _Templates._files[fileName] = file.read()
            else:
                newFilePath = filePath.replace(".xhtml", ".mako")
                _Templates._files[fileName] = mako.template.Template(filename=newFilePath, input_encoding="utf-8", output_encoding="utf-8")


class Ebook(Options):
    OPTIONS = [Option(name="includeOptionalFiles",
                      value=True,
                      description="Indica si los archivos opcionales (dedicatoria.xhtml, autor.xhtml y autor.jpg) deben incluirse en el epub "
                                  "incluso si dichos campos no fueron ingresados.")]

    _epubBase = _Templates(config.EPUBBASE_FILES_DIR_PATH)

    def __init__(self, ebookData, metadata=None, **options):
        super().__init__(**options)

        # Debería hacer una copia profunda de ebookData también técnicamente, ya que más adelante
        # modifico su objecto toc. Esto es prohibitivo, dado que estaría creando una copia de todas
        # las secciones inútilmente. Lo que podría hacer es generar una copia de la toc aparte, ya
        # que es lo único que necesito modificar.
        self._ebookData = ebookData or ebook_data.EbookData()
        self._metadata = copy.deepcopy(metadata) if metadata else ebook_metadata.Metadata()

        # Guardo una referencia a la sección de notas, si la hay, para facilitarme luego alguas comprobaciones.
        self._notesSection = self._ebookData.sections[-1] if (self._ebookData.sections and
                                                              type(self._ebookData.sections[-1]) == ebook_data.NotesSection) else None

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

        # Compruebo si estoy ante un string (o sea, un directorio) o un objeto file-like.
        if isinstance(file, str):
            fileName = os.path.join(file, epubName)
            outputEpub.generate(fileName)
            return fileName
        else:
            outputEpub.generate(file)
            return epubName

    def _addEpubBaseFiles(self, outputEpub):
        publicationYear = self._metadata.publicationDate.year if self._metadata.publicationDate else ""

        author = self._getPersonsListAsText(self._metadata.authors)[0]
        translator = self._getPersonsListAsText(self._metadata.translators)[0]
        ilustrator = self._getPersonsListAsText(self._metadata.ilustrators)[0]

        # Agrego los xhtml requeridos, excepto autor.xhtml, que debe ir despúes de las secciones.
        outputEpub.addHtmlData(epubbase_names.COVER_FILENAME, Ebook._epubBase.getCover())
        outputEpub.addHtmlData(epubbase_names.SYNOPSIS_FILENAME, Ebook._epubBase.getSynopsis(self._metadata.synopsis))
        outputEpub.addHtmlData(epubbase_names.TITLE_FILENAME, Ebook._epubBase.getTitle(author,
                                                                                       self._metadata.title,
                                                                                       self._metadata.subtitle,
                                                                                       self._metadata.editor,
                                                                                       self._metadata.collectionName,
                                                                                       self._metadata.subCollectionName,
                                                                                       self._metadata.collectionVolume))
        outputEpub.addHtmlData(epubbase_names.INFO_FILENAME, Ebook._epubBase.getInfo(self._metadata.originalTitle,
                                                                                     author,
                                                                                     publicationYear,
                                                                                     translator,
                                                                                     ilustrator,
                                                                                     self._metadata.coverDesigner,
                                                                                     self._metadata.coverModification,
                                                                                     self._metadata.editor))

        if self._metadata.dedication or self._options.includeOptionalFiles:
            outputEpub.addHtmlData(epubbase_names.DEDICATION_FILENAME, Ebook._epubBase.getDedication(self._metadata.dedication))

        outputEpub.addImageData(epubbase_names.COVER_IMAGE_FILENAME, self._metadata.coverImage)

        authorsWithBiographyOrImage = (a for a in self._metadata.authors if a.biography or a.image)
        for i, author in enumerate(authorsWithBiographyOrImage):
            outputEpub.addImageData(epubbase_names.generateAuthorImageFileName(i), author.image)

        # Agrego el resto de los archivos del epubbase.
        outputEpub.addImageData(epubbase_names.EPL_LOGO_FILENAME, Ebook._epubBase.getEplLogoImage())
        outputEpub.addImageData(epubbase_names.EX_LIBRIS_FILENAME, Ebook._epubBase.getExLibrisImage())
        outputEpub.addStyleData(epubbase_names.STYLE_FILENAME, Ebook._epubBase.getCss())
        outputEpub.addMetaFile(epubbase_names.IBOOKS_DISPLAY_OPTIONS_FILE_NAME, Ebook._epubBase.getIBooksDisplayOptionsFile())

    def _addSections(self, outputEpub):
        for section in self._ebookData.sections[:-1] if self._notesSection else self._ebookData.sections:
            outputEpub.addHtmlData(section.name, section.toHtml())

        authorsWithBiographyOrImage = (a for a in self._metadata.authors if a.biography or a.image)
        for i, author in enumerate(authorsWithBiographyOrImage):
            title = self._getTocTitleForAuthorFile() if i == 0 else None
            imageName = epubbase_names.generateAuthorImageFileName(i)

            authorContent = Ebook._epubBase.getAuthor(author.biography, title, imageName)
            outputEpub.addHtmlData(epubbase_names.generateAuthorFileName(i), authorContent)

        if self._notesSection:
            outputEpub.addHtmlData(self._notesSection.name, self._notesSection.toHtml())

    def _addImages(self, outputEpub):
        for image in self._ebookData.images:
            outputEpub.addImageData(image.name, image.content)

    def _addMetadata(self, outputEpub):
        author = self._getPersonsListAsText(self._metadata.authors)

        # Agrego semántica a cubierta.xhtml.
        outputEpub.addReference(epubbase_names.COVER_FILENAME, "Cover", "cover")

        # Es necesario agregarle semántica a cover.jpg, sino algunos ereaders no la reconocen como imagen de portada.
        outputEpub.addCustomMetadata("cover", epubbase_names.COVER_IMAGE_FILENAME)

        outputEpub.addTitle(self._metadata.title)
        outputEpub.addAuthor(author[0], author[1])
        outputEpub.addLanguage(self._metadata.language)

        if self._metadata.synopsis == ebook_metadata.Metadata.DEFAULT_SYNOPSIS:
            outputEpub.addDescription("Sinopsis")
        else:
            # En la sinopsis (el campo description) en los metadatos, no puedo tener saltos de línea. Podría directamente
            # eliminarlos, pero entonces el texto del párrafo B quedaría pegado al del párrafo A. Por eso es que reemplazo
            # los saltos de línea por un espacio.
            outputEpub.addDescription(utils.removeTags(self._metadata.synopsis.replace("\n", " ")))

        outputEpub.addPublisher("ePubLibre")

        if self._metadata.genres:
            # Ordeno los géneros alfabéticamente.
            self._metadata.genres.sort(key=lambda x: (x.genreType, x.genre, x.subGenre))

            genres = []
            previousGenre = ""
            for genre in self._metadata.genres:
                if genre.genre != previousGenre:
                    genres.append(genre.genre)
                    previousGenre = genre.genre
                genres.append(genre.subGenre)

            outputEpub.addSubject(", ".join(genres))

        if self._metadata.translators:
            translator = self._getPersonsListAsText(self._metadata.translators)
            outputEpub.addTranslator(translator[0], translator[1])

        if self._metadata.ilustrators:
            ilustrator = self._getPersonsListAsText(self._metadata.ilustrators)
            outputEpub.addIlustrator(ilustrator[0], ilustrator[1])

        if self._metadata.publicationDate is not None:
            outputEpub.addPublicationDate(self._metadata.publicationDate)

        if self._metadata.subCollectionName:
            calibreSeries = ""

            if self._metadata.collectionName:
                calibreSeries += "{0}: ".format(self._metadata.collectionName)
            calibreSeries += self._metadata.subCollectionName

            try:
                # Elimino los ceros a la izquierda si se trata de un número.
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
        # La cubierta debe ser la primera entrada en la toc.
        outputEpub.addNavPoint(epubbase_names.COVER_FILENAME, "Cubierta")

        # El título del libro debe ser la segunda entrada en la toc.
        outputEpub.addNavPoint(epubbase_names.TITLE_FILENAME, self._metadata.title)

        if any(a for a in self._metadata.authors if a.biography or a.image):
            self._ebookData.toc.addFirstLevelTitle(epubbase_names.AUTHOR_FILENAME, self._getTocTitleForAuthorFile(), False)

        if self._notesSection:
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
        fileName.append(" [{0}] (r1.0 {1})".format(self._metadata.bookId, self._metadata.editor))

        return utils.removeSpecialCharacters("{0}.epub".format("".join(fileName)))

    def _setDefaultMetadata(self):
        if not self._metadata.synopsis:
            self._metadata.synopsis = ebook_metadata.Metadata.DEFAULT_SYNOPSIS

        if not self._metadata.title:
            self._metadata.title = ebook_metadata.Metadata.DEFAULT_TITLE

        if not self._metadata.dedication and self._options.includeOptionalFiles:
            self._metadata.dedication = ebook_metadata.Metadata.DEFAULT_DEDICATION

        if not self._metadata.bookId:
            self._metadata.bookId = ebook_metadata.Metadata.DEFAULT_BOOK_ID

        if not self._metadata.editor:
            self._metadata.editor = ebook_metadata.Metadata.DEFAULT_EDITOR

        if not self._metadata.language:
            self._metadata.language = ebook_metadata.Metadata.DEFAULT_LANGUAGE

        if not self._metadata.genres:
            # El tipo de género no interesa, dado que no aparece en los metadatos del epub.
            self._metadata.genres.append(ebook_metadata.Genre("bla", "Género", "Subgéneros"))

        if not self._metadata.coverModification:
            self._metadata.coverModification = ebook_metadata.Metadata.DEFAULT_COVER_MODIFICATION

        if not self._metadata.coverImage:
            self._metadata.coverImage = Ebook._epubBase.getCoverImage()

        if not self._metadata.authors:
            self._metadata.authors.append(ebook_metadata.Person(ebook_metadata.Metadata.DEFAULT_AUTHOR, ebook_metadata.Metadata.DEFAULT_AUTHOR))

        # Veo a qué autor debo agregarle su biografía o imagen para que se incluya autor.xhtml y autor.jpg.
        for author in self._metadata.authors:
            if author.biography or author.image or self._options.includeOptionalFiles:
                if not author.biography:
                    author.biography = ebook_metadata.Metadata.DEFAULT_AUTHOR_BIOGRAPHY
                if not author.image:
                    author.image = Ebook._epubBase.getAuthorImage()

    def _getPersonsListAsText(self, persons):
        """
        Convierte una lista de Person a texto. Cada Person se concatena con un & (ampersand).

        @param persons: una lista de Person.

        @return: una tupla cuyo primer elemento es un string concatenado con todos los nombres, y el
                 segundo un string concatenado con todos los file-as.
        """
        return " & ".join((p.name for p in persons)), " & ".join((p.fileAs for p in persons))

    def _getTocTitleForAuthorFile(self):
        authors = self._metadata.authors

        if not authors or (len(authors) == 1 and authors[0].gender == ebook_metadata.Person.MALE_GENDER):
            return "Autor"
        else:
            return "Autores" if len(authors) > 1 else "Autora"