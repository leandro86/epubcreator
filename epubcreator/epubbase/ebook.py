import os
import copy

import mako.template
from lxml import etree

from epubcreator.pyepub.pyepubwriter import epub
from epubcreator.epubbase import ebook_metadata, ebook_data, names
from epubcreator.misc import utils
from epubcreator.misc.options import Options, Option


class _Templates:
    _files = {}

    def __init__(self):
        if not _Templates._files:
            _Templates._loadEpubBaseFiles()

    def getCover(self):
        return _Templates._files[names.COVER_FILENAME]

    def getSynopsis(self, synopsis):
        template = _Templates._files[names.SYNOPSIS_FILENAME]
        return template.render(synopsis=synopsis)

    def getTitle(self, author, title, subtitle, editor, collectionName, subCollectionName, collectionVolume):
        template = _Templates._files[names.TITLE_FILENAME]
        return template.render(author=author, title=title, subtitle=subtitle, editor=editor, collectionName=collectionName,
                               subCollectionName=subCollectionName, collectionVolume=collectionVolume)

    def getInfo(self, originalTitle, author, publicationYear, translator, ilustrator, coverDesigner, coverModification, editor):
        template = _Templates._files[names.INFO_FILENAME]
        return template.render(originalTitle=originalTitle, author=author, publicationYear=publicationYear, translator=translator,
                               ilustrator=ilustrator, coverDesigner=coverDesigner, coverModification=coverModification, editor=editor)

    def getDedication(self, dedication):
        template = _Templates._files[names.DEDICATION_FILENAME]
        return template.render(dedication=dedication)

    def getAuthor(self, authorBiography, title, imageName):
        template = _Templates._files[names.AUTHOR_FILENAME]
        return template.render(authorBiography=authorBiography, title=title, imageName=imageName)

    def getEplLogoImage(self):
        return _Templates._files[names.EPL_LOGO_FILENAME]

    def getExLibrisImage(self):
        return _Templates._files[names.EX_LIBRIS_FILENAME]

    def getCss(self):
        return _Templates._files[names.STYLE_FILENAME]

    def getCoverImage(self):
        return _Templates._files[names.COVER_IMAGE_FILENAME]

    def getAuthorImage(self):
        return _Templates._files[names.AUTHOR_IMAGE_FILENAME]

    def getIBooksDisplayOptionsFile(self):
        return _Templates._files[names.IBOOKS_DISPLAY_OPTIONS_FILE_NAME]

    @staticmethod
    def _loadEpubBaseFiles():
        templates = (names.AUTHOR_FILENAME,
                     names.DEDICATION_FILENAME,
                     names.INFO_FILENAME,
                     names.SYNOPSIS_FILENAME,
                     names.TITLE_FILENAME)

        noTemplates = (names.COVER_FILENAME,
                       names.STYLE_FILENAME,
                       names.IBOOKS_DISPLAY_OPTIONS_FILE_NAME,
                       names.EPL_LOGO_FILENAME,
                       names.EX_LIBRIS_FILENAME,
                       names.AUTHOR_IMAGE_FILENAME,
                       names.COVER_IMAGE_FILENAME)

        for fileName in templates:
            filePath = names.getFullPathToFile(fileName)
            newFilePath = filePath.replace(".xhtml", ".mako")
            _Templates._files[fileName] = mako.template.Template(filename=newFilePath, input_encoding="utf-8", output_encoding="utf-8")

        for fileName in noTemplates:
            filePath = names.getFullPathToFile(fileName)
            with open(filePath, "rb") as file:
                _Templates._files[fileName] = file.read()


class Ebook(Options):
    OPTIONS = [Option(name="includeOptionalFiles",
                      value=True,
                      description="Indica si los archivos opcionales (dedicatoria.xhtml y autor.xhtml) deben incluirse en el epub "
                                  "incluso si los respectivos campos no fueron ingresados.")]

    _epubBase = _Templates()

    def __init__(self, ebookData, metadata=None, **options):
        super().__init__(**options)

        self._ebookData = ebookData or ebook_data.EbookData()
        self._metadata = copy.deepcopy(metadata) if metadata else ebook_metadata.Metadata()

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
        self._addSectionsAndToc(outputEpub)
        self._addImages(outputEpub)
        self._addMetadata(outputEpub)

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
        outputEpub.addHtmlData(names.COVER_FILENAME, Ebook._epubBase.getCover())
        outputEpub.addHtmlData(names.SYNOPSIS_FILENAME, Ebook._epubBase.getSynopsis(self._metadata.synopsis))
        outputEpub.addHtmlData(names.TITLE_FILENAME, Ebook._epubBase.getTitle(author,
                                                                              self._metadata.title,
                                                                              self._metadata.subtitle,
                                                                              self._metadata.editor,
                                                                              self._metadata.collectionName,
                                                                              self._metadata.subCollectionName,
                                                                              self._metadata.collectionVolume))
        outputEpub.addHtmlData(names.INFO_FILENAME, Ebook._epubBase.getInfo(self._metadata.originalTitle,
                                                                            author,
                                                                            publicationYear,
                                                                            translator,
                                                                            ilustrator,
                                                                            self._metadata.coverDesigner,
                                                                            self._metadata.coverModification,
                                                                            self._metadata.editor))

        if self._metadata.dedication or self._options.includeOptionalFiles:
            outputEpub.addHtmlData(names.DEDICATION_FILENAME, Ebook._epubBase.getDedication(self._metadata.dedication))

        outputEpub.addImageData(names.COVER_IMAGE_FILENAME, self._metadata.coverImage)

        authorsWithBiographyOrImage = (a for a in self._metadata.authors if a.biography or a.image)
        for i, author in enumerate(authorsWithBiographyOrImage):
            outputEpub.addImageData(names.generateAuthorImageFileName(i), author.image)

        # Agrego el resto de los archivos del epubbase.
        outputEpub.addImageData(names.EPL_LOGO_FILENAME, Ebook._epubBase.getEplLogoImage())
        outputEpub.addImageData(names.EX_LIBRIS_FILENAME, Ebook._epubBase.getExLibrisImage())
        outputEpub.addStyleData(names.STYLE_FILENAME, Ebook._epubBase.getCss())
        outputEpub.addMetaFile(names.IBOOKS_DISPLAY_OPTIONS_FILE_NAME, Ebook._epubBase.getIBooksDisplayOptionsFile())

    def _addSectionsAndToc(self, outputEpub):
        def processSections(sections):
            navPoints = []
            previousLevel = "1"

            for section in sections:
                outputEpub.addHtmlData(section.name, section.toHtml())
                hs = section.xpath("//h1 | //h2 | //h3 | //h4 | //h5 | //h6")

                for h in hs:
                    currentLevel = h.tag[-1]

                    titleText = self._getTitleText(h)
                    titleId = h.get("id")
                    titleSrc = "{0}{1}".format(section.name, "#" + titleId if titleId else "")

                    if currentLevel == "1":
                        navPoints.append(outputEpub.addNavPoint(titleSrc, titleText))
                    else:
                        if currentLevel < previousLevel:
                            for i in range(int(previousLevel) - int(currentLevel) + 1):
                                navPoints.pop()
                        elif currentLevel == previousLevel:
                            navPoints.pop()

                        childNavPoint = navPoints[-1].addNavPoint(titleSrc, titleText)
                        navPoints.append(childNavPoint)

                    previousLevel = currentLevel

        # La cubierta debe ser la primera entrada en la toc.
        outputEpub.addNavPoint(names.COVER_FILENAME, "Cubierta")

        # El título del libro debe ser la segunda entrada en la toc.
        outputEpub.addNavPoint(names.TITLE_FILENAME, self._metadata.title)

        processSections(self._ebookData.iterTextSections())

        authorsWithBiographyOrImage = [a for a in self._metadata.authors if a.biography or a.image]
        if authorsWithBiographyOrImage:
            outputEpub.addNavPoint(names.AUTHOR_FILENAME, self._getTocTitleForAuthorFile())

            for i, author in enumerate(authorsWithBiographyOrImage):
                title = self._getTocTitleForAuthorFile() if i == 0 else None
                imageName = names.generateAuthorImageFileName(i)

                authorContent = Ebook._epubBase.getAuthor(author.biography, title, imageName)
                outputEpub.addHtmlData(names.generateAuthorFileName(i), authorContent)

        processSections(self._ebookData.iterNotesSections())

    def _addImages(self, outputEpub):
        for image in self._ebookData.iterImages():
            outputEpub.addImageData(image.name, image.content)

    def _addMetadata(self, outputEpub):
        author = self._getPersonsListAsText(self._metadata.authors)

        # Agrego semántica a cubierta.xhtml.
        outputEpub.addReference(names.COVER_FILENAME, "Cover", "cover")

        # Es necesario agregarle semántica a cover.jpg, sino algunos ereaders no la reconocen como imagen de portada.
        outputEpub.addCustomMetadata("cover", names.COVER_IMAGE_FILENAME)

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

    def _getTitleText(self, h):
        """
        Retorna el texto de un título, reemplazando los tags "br" por un espacio.
        """
        if h.xpath("descendant::br"):
            # No puedo modificar el element "h" directamente, sino que necesito
            # trabajar sobre una copia. Una deep copy es otra opción, pero creo
            # que va a terminar copiando todoo el tree...
            h = etree.fromstring(etree.tostring(h))

            for br in h.xpath("descendant::br"):
                br.text = " "

            etree.strip_tags(h, "br")

        return "".join(h.xpath("descendant::text()"))