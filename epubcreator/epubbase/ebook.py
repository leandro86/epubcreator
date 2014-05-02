import os

from lxml import etree

from epubcreator.pyepub.pyepubwriter import epub
from epubcreator.epubbase import ebook_metadata, ebook_data, files, images
from epubcreator.misc import utils
from epubcreator.misc.options import Options, Option


class Ebook(Options):
    OPTIONS = [Option(name="includeOptionalFiles",
                      value=True,
                      description="Indica si los archivos opcionales (dedicatoria.xhtml y autor.xhtml) deben incluirse en el epub "
                                  "incluso si los respectivos campos no fueron ingresados.")]

    def __init__(self, ebookData, metadata=None, **options):
        super().__init__(**options)

        self._ebookData = ebookData or ebook_data.EbookData()
        self._metadata = metadata or ebook_metadata.Metadata()

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
        synopsis = self._metadata.synopsis or ebook_metadata.Metadata.DEFAULT_SYNOPSIS
        title = self._metadata.title or ebook_metadata.Metadata.DEFAULT_TITLE
        editor = self._metadata.editor or ebook_metadata.Metadata.DEFAULT_EDITOR
        coverModification = self._metadata.coverModification or ebook_metadata.Metadata.DEFAULT_COVER_MODIFICATION
        coverImage = self._metadata.coverImage or images.CoverImage(files.EpubBaseFiles.getFile(files.EpubBaseFiles.COVER_IMAGE_FILENAME))
        publicationYear = self._metadata.publicationDate.year if self._metadata.publicationDate else ""
        authors = self._metadata.authors or [ebook_metadata.Person(ebook_metadata.Metadata.DEFAULT_AUTHOR, ebook_metadata.Metadata.DEFAULT_AUTHOR)]
        author = self._getPersonsListAsText(authors)[0]
        translator = self._getPersonsListAsText(self._metadata.translators)[0]
        ilustrator = self._getPersonsListAsText(self._metadata.ilustrators)[0]

        # Agrego los xhtml requeridos, excepto autor.xhtml, que debe ir despúes de las secciones.
        outputEpub.addHtmlData(files.EpubBaseFiles.COVER_FILENAME, files.EpubBaseFiles.getFile(files.EpubBaseFiles.COVER_FILENAME))
        outputEpub.addHtmlData(files.EpubBaseFiles.SYNOPSIS_FILENAME, files.EpubBaseFiles.getSynopsis(synopsis))
        outputEpub.addHtmlData(files.EpubBaseFiles.TITLE_FILENAME, files.EpubBaseFiles.getTitle(author,
                                                                                                title,
                                                                                                self._metadata.subtitle,
                                                                                                editor,
                                                                                                self._metadata.collectionName,
                                                                                                self._metadata.subCollectionName,
                                                                                                self._metadata.collectionVolume))
        outputEpub.addHtmlData(files.EpubBaseFiles.INFO_FILENAME, files.EpubBaseFiles.getInfo(self._metadata.originalTitle,
                                                                                              author,
                                                                                              publicationYear,
                                                                                              translator,
                                                                                              ilustrator,
                                                                                              self._metadata.coverDesigner,
                                                                                              coverModification,
                                                                                              editor))

        if self._metadata.dedication or self._options.includeOptionalFiles:
            dedication = self._metadata.dedication or ebook_metadata.Metadata.DEFAULT_DEDICATION
            outputEpub.addHtmlData(files.EpubBaseFiles.DEDICATION_FILENAME, files.EpubBaseFiles.getDedication(dedication))

        outputEpub.addImageData(files.EpubBaseFiles.COVER_IMAGE_FILENAME, coverImage.toBytes())

        # Agrego el resto de los archivos del epubbase.
        outputEpub.addImageData(files.EpubBaseFiles.EPL_LOGO_FILENAME, files.EpubBaseFiles.getFile(files.EpubBaseFiles.EPL_LOGO_FILENAME))
        outputEpub.addImageData(files.EpubBaseFiles.EX_LIBRIS_FILENAME, files.EpubBaseFiles.getFile(files.EpubBaseFiles.EX_LIBRIS_FILENAME))
        outputEpub.addStyleData(files.EpubBaseFiles.STYLE_FILENAME, files.EpubBaseFiles.getFile(files.EpubBaseFiles.STYLE_FILENAME))
        outputEpub.addMetaFile(files.EpubBaseFiles.APPLE_XML, files.EpubBaseFiles.getFile(files.EpubBaseFiles.APPLE_XML))

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
        outputEpub.addNavPoint(files.EpubBaseFiles.COVER_FILENAME, "Cubierta")

        # El título del libro debe ser la segunda entrada en la toc.
        outputEpub.addNavPoint(files.EpubBaseFiles.TITLE_FILENAME, self._metadata.title or ebook_metadata.Metadata.DEFAULT_TITLE)

        processSections(self._ebookData.iterTextSections())

        authors = self._metadata.authors or [ebook_metadata.Person(ebook_metadata.Metadata.DEFAULT_AUTHOR, ebook_metadata.Metadata.DEFAULT_AUTHOR)]

        # Veo a qué autor debo agregarle su biografía o imagen para que se incluya autor.xhtml y autor.jpg.
        for author in authors:
            if author.biography or author.image or self._options.includeOptionalFiles:
                if not author.biography:
                    author.biography = ebook_metadata.Metadata.DEFAULT_AUTHOR_BIOGRAPHY
                if not author.image:
                    author.image = images.AuthorImage(files.EpubBaseFiles.getFile(files.EpubBaseFiles.AUTHOR_IMAGE_FILENAME), allowProcessing=False)

        authorsWithBiographyOrImage = [a for a in authors if a.biography or a.image]
        if authorsWithBiographyOrImage:
            outputEpub.addNavPoint(files.EpubBaseFiles.AUTHOR_FILENAME, self._getTocTitleForAuthorFile(authors))

            for i, author in enumerate(authorsWithBiographyOrImage):
                title = self._getTocTitleForAuthorFile(authors) if i == 0 else None
                imageName = files.EpubBaseFiles.generateAuthorImageFileName(i)
                authorContent = files.EpubBaseFiles.getAuthor(author.biography, title, imageName)

                outputEpub.addHtmlData(files.EpubBaseFiles.generateAuthorFileName(i), authorContent)
                outputEpub.addImageData(imageName, author.image.toBytes())

        processSections(self._ebookData.iterNotesSections())

    def _addImages(self, outputEpub):
        for image in self._ebookData.iterImages():
            outputEpub.addImageData(image.name, image.content)

    def _addMetadata(self, outputEpub):
        authors = self._metadata.authors or [ebook_metadata.Person(ebook_metadata.Metadata.DEFAULT_AUTHOR, ebook_metadata.Metadata.DEFAULT_AUTHOR)]
        author = self._getPersonsListAsText(authors)

        # Agrego semántica a cubierta.xhtml.
        outputEpub.addReference(files.EpubBaseFiles.COVER_FILENAME, "Cover", "cover")

        # Es necesario agregarle semántica a cover.jpg, sino algunos ereaders no la reconocen como imagen de portada.
        outputEpub.addCustomMetadata("cover", files.EpubBaseFiles.COVER_IMAGE_FILENAME)

        outputEpub.addTitle(self._metadata.title or ebook_metadata.Metadata.DEFAULT_TITLE)
        outputEpub.addAuthor(author[0], author[1])
        outputEpub.addLanguage(self._metadata.language or ebook_metadata.Metadata.DEFAULT_LANGUAGE)

        if self._metadata.synopsis:
            # En la sinopsis (el campo description) en los metadatos, no puedo tener saltos de línea. Podría directamente
            # eliminarlos, pero entonces el texto del párrafo B quedaría pegado al del párrafo A. Por eso es que reemplazo
            # los saltos de línea por un espacio.
            outputEpub.addDescription(utils.removeTags(self._metadata.synopsis.replace("\n", " ")))
        else:
            outputEpub.addDescription("Sinopsis")

        outputEpub.addPublisher("ePubLibre")

        # El tipo de género no interesa si debo poner uno por defecto, dado que no aparece en los metadatos del epub.
        genres = self._metadata.genres or [ebook_metadata.Genre("bla", "Género", "Subgéneros")]

        # Ordeno los géneros alfabéticamente.
        genres.sort(key=lambda x: (x.genreType, x.genre, x.subGenre))

        genresText = []
        previousGenre = ""
        for genre in genres:
            if genre.genre != previousGenre:
                genresText.append(genre.genre)
                previousGenre = genre.genre
            genresText.append(genre.subGenre)

        outputEpub.addSubject(", ".join(genresText))

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
        authors = self._metadata.authors or [ebook_metadata.Person(ebook_metadata.Metadata.DEFAULT_AUTHOR, ebook_metadata.Metadata.DEFAULT_AUTHOR)]

        fileName = []
        authorsFileAs = [author.fileAs for author in authors]
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

        fileName.append(self._metadata.title or ebook_metadata.Metadata.DEFAULT_TITLE)

        bookId = self._metadata.bookId or ebook_metadata.Metadata.DEFAULT_BOOK_ID
        editor = self._metadata.editor or ebook_metadata.Metadata.DEFAULT_EDITOR
        fileName.append(" [{0}] (r1.0 {1})".format(bookId, editor))

        return utils.removeSpecialCharacters("{0}.epub".format("".join(fileName)))

    def _getPersonsListAsText(self, persons):
        """
        Convierte una lista de Person a texto. Cada Person se concatena con un & (ampersand).

        @param persons: una lista de Person.

        @return: una tupla cuyo primer elemento es un string concatenado con todos los nombres, y el
                 segundo un string concatenado con todos los file-as.
        """
        return " & ".join((p.name for p in persons)), " & ".join((p.fileAs for p in persons))

    def _getTocTitleForAuthorFile(self, authors):
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