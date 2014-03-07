import unittest
import tempfile
import datetime

from lxml import etree
from pyepub.pyepubreader import epub

from epubcreator import ebook, ebook_data, ebook_metadata, epubbase_names


class EbookTests(unittest.TestCase):
    _NAMESPACES = {"x": "http://www.w3.org/1999/xhtml"}

    def setUp(self):
        self._outputFile = tempfile.TemporaryFile()
        self._metadata = ebook_metadata.Metadata()
        self._outputEpub = None

    def tearDown(self):
        self._outputFile.close()

        if self._outputEpub:
            self._outputEpub.close()

    def test_cover_file(self):
        self._generateEbook()
        self._getCoverFile()

        self.assertTrue(self._outputEpub.hasFile(epubbase_names.COVER_FILENAME))

    def test_title_file_data(self):
        self._metadata.authors.append(ebook_metadata.Person("el autor", "el autor"))
        self._metadata.title = "el título"
        self._metadata.subtitle = "el subtítulo"
        self._metadata.editor = "el editor"

        self._generateEbook()
        title = self._getTitleFile()

        self.assertEqual(self._xpath(title, "/x:html/x:body/x:p[@class = 'tautor']/text()"), ["el autor"])
        self.assertEqual(self._xpath(title, "/x:html/x:body/x:h1[@class = 'ttitulo']/text()"), ["el título"])
        self.assertEqual(self._xpath(title, "/x:html/x:body/x:p[@class = 'tsubtitulo']/text()"), ["el subtítulo"])
        self.assertEqual(self._xpath(title, "/x:html/x:body/x:p[@class = 'tfirma']/text()"), ["el editor "])
        self.assertEqual(self._xpath(title, "/x:html/x:body/x:p[@class = 'tfirma']/x:span[@class = 'tfecha']/text()"),
                         [datetime.datetime.now().strftime("%d.%m.%y")])

    def test_info_file_data(self):
        self._metadata.originalTitle = "el título original"
        self._metadata.authors.append(ebook_metadata.Person("el autor", "el autor"))
        self._metadata.publicationDate = datetime.date(1756, 1, 1)
        self._metadata.translators.append(ebook_metadata.Person("el traductor", "el traductor"))
        self._metadata.ilustrators.append(ebook_metadata.Person("el ilustrador", "el ilustrador"))
        self._metadata.coverDesignOrTweak = "Diseño"
        self._metadata.coverDesigner = "el diseñador de cubierta"
        self._metadata.editor = "el editor"

        self._generateEbook()
        info = self._getInfoFile()

        self.assertEqual(self._xpath(info, "/x:html/x:body/x:div[@class = 'info']/x:p[1]/text()"),
                         ["Título original: "])
        self.assertEqual(self._xpath(info, "/x:html/x:body/x:div[@class = 'info']/x:p[1]/x:em/text()"),
                         ["el título original"])

        self.assertEqual(self._xpath(info, "/x:html/x:body/x:div[@class = 'info']/x:p[2]/text()"), ["el autor, 1756"])
        self.assertEqual(self._xpath(info, "/x:html/x:body/x:div[@class = 'info']/x:p[3]/text()"),
                         ["Traducción: el traductor"])
        self.assertEqual(self._xpath(info, "/x:html/x:body/x:div[@class = 'info']/x:p[4]/text()"),
                         ["Ilustraciones: el ilustrador"])
        self.assertEqual(self._xpath(info, "/x:html/x:body/x:div[@class = 'info']/x:p[5]/text()"),
                         ["Diseño de cubierta: el diseñador de cubierta"])
        self.assertEqual(self._xpath(info, "/x:html/x:body/x:div[@class = 'info']/x:p[@class = 'salto10']/text()"),
                         ["Editor digital: el editor"])

    def test_synopsis_file_data(self):
        self._metadata.synopsis = "Párrafo 1 de la sinopsis.\nPárrafo 2 de la sinopsis.\nPárrafo 3 de la sinopsis."

        self._generateEbook()
        synopsis = self._getSynopsisFile()

        self.assertEqual(self._xpath(synopsis, "/x:html/x:body/x:div[@class = 'sinopsis']/x:p[1]/text()"),
                         ["Párrafo 1 de la sinopsis."])
        self.assertEqual(self._xpath(synopsis, "/x:html/x:body/x:div[@class = 'sinopsis']/x:p[2]/text()"),
                         ["Párrafo 2 de la sinopsis."])
        self.assertEqual(self._xpath(synopsis, "/x:html/x:body/x:div[@class = 'sinopsis']/x:p[3]/text()"),
                         ["Párrafo 3 de la sinopsis."])

    def test_dedication_file_data(self):
        self._metadata.dedication = ("Párrafo 1 de la dedicatoria.\nPárrafo 2 de la dedicatoria.\nPárrafo 3 de "
                                     "la dedicatoria.")

        self._generateEbook()
        dedication = self._getDedicationFile()

        self.assertEqual(self._xpath(dedication, "/x:html/x:body/x:div[@class = 'dedicatoria']/x:p[1]/text()"),
                         ["Párrafo 1 de la dedicatoria."])
        self.assertEqual(self._xpath(dedication, "/x:html/x:body/x:div[@class = 'dedicatoria']/x:p[2]/text()"),
                         ["Párrafo 2 de la dedicatoria."])
        self.assertEqual(self._xpath(dedication, "/x:html/x:body/x:div[@class = 'dedicatoria']/x:p[3]/text()"),
                         ["Párrafo 3 de la dedicatoria."])

    def test_not_subtitle_on_title_data(self):
        self._generateEbook()
        title = self._getTitleFile()

        self.assertFalse(self._xpath(title, "/x:html/x:body/x:p[@class = 'tsubtitulo']"))

        # En titulo.xhtml hay un comentario indicando en el campo de subtítulo que es opcional, por eso debo verificar
        # que también ese comentario se haya borrado
        self.assertFalse(self._xpath(title, "/x:html/x:body/comment()"))

    def test_missing_fields_on_info_data(self):
        self._generateEbook()
        info = self._getInfoFile()

        self.assertFalse(self._xpath(info,
                                     "/x:html/x:body/x:div[@class = 'info']/x:p[contains(text(), 'Título original')]"))

        # Si no pongo una fecha de publicación original, entonces en el campo de autor solo debe figurar
        # el autor, y nada más
        self.assertEqual(self._xpath(info,
                                     "/x:html/x:body/x:div[@class = 'info']/x:p[contains(text(), 'Autor')]/text()")[0],
                         "Autor")

        self.assertFalse(self._xpath(info,
                                     "/x:html/x:body/x:div[@class = 'info']/x:p[contains(text(), 'Traducción')]"))
        self.assertFalse(self._xpath(info,
                                     "/x:html/x:body/x:div[@class = 'info']/x:p[contains(text(), 'Ilustraciones')]"))
        self.assertFalse(self._xpath(info,
                                     "/x:html/x:body/x:div[@class = 'info']/x:p[contains(text(), 'Diseño/Retoque')]"))

        # Debo comprobar que el comentario asociado al campo diseñador de portada haya sido eliminado también
        comments = self._xpath(info, "/x:html/x:body/x:div[@class = 'info']/comment()")
        self.assertFalse(any("usar la palabra «Diseño» si la portada" in str(c) for c in comments))

    def test_synopsis_file_exists_if_not_synopsis_text(self):
        self._generateEbook()
        synopsis = self._getSynopsisFile()

        # Si no agrego un texto de sinopsis, entonces por ahora agrego igualmente sinopsis.xhtml al epub, con el texto
        # que viene por defecto en el base.
        self.assertTrue(self._xpath(synopsis,
                                    "/x:html/x:body/x:div[@class = 'sinopsis']/x:p[1]/text()")[0]
                        .startswith("Yo por bien tengo que cosas tan señaladas"))

    def test_dedication_file_exists_if_not_dedication_text(self):
        self._generateEbook()
        dedication = self._getDedicationFile()

        # Al igual que en la sinopsis, si no agregué texto de dedicatoria, igualmente agrego dedicatoria.xhtml
        self.assertTrue(self._xpath(dedication, "/x:html/x:body/x:div[@class = 'dedicatoria']/x:p[1]/text()")[0]
                        .startswith("Suspiró entonces mío Cid"))

    def test_author_file_data(self):
        self._metadata.authorBiography = ("Párrafo 1 de la biografía.\nPárrafo 2 de la biografía.\nPárrafo 3 de "
                                          "la biografía.")

        self._generateEbook()
        author = self._getAuthorFile()

        self.assertEqual(self._xpath(author, "/x:html/x:body/x:div[@class = 'autor']/x:p[position() = 1]/text()"),
                         ["Párrafo 1 de la biografía."])
        self.assertEqual(self._xpath(author, "/x:html/x:body/x:div[@class = 'autor']/x:p[position() = 2]/text()"),
                         ["Párrafo 2 de la biografía."])
        self.assertEqual(self._xpath(author, "/x:html/x:body/x:div[@class = 'autor']/x:p[position() = 3]/text()"),
                         ["Párrafo 3 de la biografía."])

        # Compruebo que exista la imagen del autor, ya que autor.xhtml la referencia
        try:
            self._outputEpub.read("OEBPS/Images/{0}".format(epubbase_names.AUTHOR_IMAGE_FILENAME))
        except KeyError as e:
            self.fail(e)

        # Compruebo que el archivo del autor sea el último (ya que así lo indica el epubbase. En realidad indica que
        # debe ser el último antes de notas.xhtml, pero acá no agrego notas, me basta con chequear por el último.)
        htmlFiles = self._outputEpub.getHtmlFileNamesReadingOrder()
        self.assertEqual(htmlFiles[-1], epubbase_names.AUTHOR_FILENAME)

    def test_author_file_exists_if_not_author_biography(self):
        self._generateEbook()
        author = self._getAuthorFile()

        paragraphs = self._xpath(author, "/x:html/x:body/x:div[@class = 'autor']/x:p")
        self.assertTrue(len(paragraphs), 2)

    def test_author_file_is_second_to_last_when_ebook_contains_notes(self):
        self._generateEbook([ebook_data.NotesSection()])

        htmlFiles = self._outputEpub.getHtmlFileNamesReadingOrder()
        self.assertEqual(htmlFiles[-2], epubbase_names.AUTHOR_FILENAME)

    def test_author_file_exists_when_ebook_contains_text_section(self):
        self._generateEbook([ebook.ebook_data.TextSection(0)])

        htmlFiles = self._outputEpub.getHtmlFileNamesReadingOrder()
        self.assertEqual(htmlFiles[-1], epubbase_names.AUTHOR_FILENAME)

    def test_multiple_authors(self):
        self._metadata.authors.append(ebook_metadata.Person("Jorge Luis Borges", "Borges, Jorge Luis"))
        self._metadata.authors.append(ebook_metadata.Person("Edgar Allan Poe", "Poe, Edgar Allan"))
        self._metadata.authors.append(ebook_metadata.Person("William Shakespeare", "Shakespeare, William"))
        self._metadata.authors.append(ebook_metadata.Person("G. K. Chesterton", "Chesterton, G. K."))

        self._generateEbook()
        info = self._getInfoFile()

        self.assertEqual(self._xpath(info, "/x:html/x:body/x:div[@class = 'info']/x:p[1]/text()"),
                         ["Jorge Luis Borges & Edgar Allan Poe & William Shakespeare & G. K. Chesterton"])

        # Compruebo que en los metadatos se hayan agregado los autores correctamente
        authors = self._outputEpub.getAuthors()
        self.assertEqual(len(authors), 1)
        self.assertEqual(authors[0], ("Jorge Luis Borges & Edgar Allan Poe & William Shakespeare & G. K. Chesterton",
                                      "Borges, Jorge Luis & Poe, Edgar Allan & Shakespeare, "
                                      "William & Chesterton, G. K."))

    def test_multiple_translators(self):
        self._metadata.translators.append(ebook_metadata.Person("Jorge Luis Borges", "Borges, Jorge Luis"))
        self._metadata.translators.append(ebook_metadata.Person("Edgar Allan Poe", "Poe, Edgar Allan"))
        self._metadata.translators.append(ebook_metadata.Person("William Shakespeare", "Shakespeare, William"))
        self._metadata.translators.append(ebook_metadata.Person("G. K. Chesterton", "Chesterton, G. K."))

        self._generateEbook()
        info = self._getInfoFile()

        self.assertEqual(self._xpath(info, "/x:html/x:body/x:div[@class = 'info']/x:p[2]/text()"),
                         ["Traducción: Jorge Luis Borges & Edgar Allan Poe & William Shakespeare & G. K. Chesterton"])

        # Compruebo que en los metadatos se hayan agregado los traductores correctamente
        translators = self._outputEpub.getTranslators()
        self.assertEqual(len(translators), 1)
        self.assertEqual(translators[0],
                         ("Jorge Luis Borges & Edgar Allan Poe & William Shakespeare & G. K. Chesterton",
                          "Borges, Jorge Luis & Poe, Edgar Allan & Shakespeare, William & Chesterton, G. K."))

    def test_multiple_ilustrators(self):
        self._metadata.ilustrators.append(ebook_metadata.Person("Jorge Luis Borges", "Borges, Jorge Luis"))
        self._metadata.ilustrators.append(ebook_metadata.Person("Edgar Allan Poe", "Poe, Edgar Allan"))
        self._metadata.ilustrators.append(ebook_metadata.Person("William Shakespeare", "Shakespeare, William"))
        self._metadata.ilustrators.append(ebook_metadata.Person("G. K. Chesterton", "Chesterton, G. K."))

        self._generateEbook()
        info = self._getInfoFile()

        self.assertEqual(self._xpath(info, "/x:html/x:body/x:div[@class = 'info']/x:p[2]/text()"),
                         ["Ilustraciones: Jorge Luis Borges & Edgar Allan Poe & William Shakespeare & G. K. "
                          "Chesterton"])

        # Compruebo que en los metadatos se hayan agregado los ilustradores correctamente
        ilustrators = self._outputEpub.getIlustrators()
        self.assertEqual(len(ilustrators), 1)
        self.assertEqual(ilustrators[0],
                         ("Jorge Luis Borges & Edgar Allan Poe & William Shakespeare & G. K. Chesterton",
                          "Borges, Jorge Luis & Poe, Edgar Allan & Shakespeare, William & Chesterton, G. K."))

    def test_simple_collection(self):
        self._metadata.subCollectionName = "Esta es la saga"
        self._metadata.collectionVolume = "9"

        self._generateEbook()

        calibreSerie = self._outputEpub.getCalibreSerie()
        self.assertEqual(calibreSerie, ("Esta es la saga", "9"))

    def test_sub_collections(self):
        self._metadata.collectionName = "Esta es la serie"
        self._metadata.subCollectionName = "Esta es la saga"
        self._metadata.collectionVolume = "9"

        self._generateEbook()

        calibreSerie = self._outputEpub.getCalibreSerie()
        self.assertEqual(calibreSerie, ("Esta es la serie: Esta es la saga", "9"))

    def test_strip_zeros_from_collection_volume_for_calibre_metadata(self):
        self._metadata.subCollectionName = "Esta es la saga"
        self._metadata.collectionVolume = "007"

        self._generateEbook()

        calibreSerie = self._outputEpub.getCalibreSerie()
        self.assertEqual(calibreSerie, ("Esta es la saga", "7"))

    def test_epub_file_name_when_one_author_and_no_collection(self):
        self._metadata.title = "Título del libro"
        self._metadata.editor = "Editor del libro"
        self._metadata.authors.append(ebook_metadata.Person("Juan Pérez", "Pérez, Juan"))

        fileName = self._generateEbook()

        self.assertEqual(fileName, "Perez, Juan - Titulo del libro (r1.0 Editor del libro).epub")

    def test_epub_file_name_when_two_authors_and_no_collection(self):
        self._metadata.title = "Título del libro"
        self._metadata.editor = "Editor del libro"
        self._metadata.authors.append(ebook_metadata.Person("Juan Pérez", "Pérez, Juan"))
        self._metadata.authors.append(ebook_metadata.Person("Roberto Gómez", "Gómez, Roberto"))

        fileName = self._generateEbook()

        self.assertEqual(fileName, "Perez, Juan & Gomez, Roberto - Titulo del libro (r1.0 Editor del libro).epub")

    def test_epub_file_name_when_three_authors_and_no_collection(self):
        self._metadata.title = "Título del libro"
        self._metadata.editor = "Editor del libro"
        self._metadata.authors.append(ebook_metadata.Person("Juan Pérez", "Pérez, Juan"))
        self._metadata.authors.append(ebook_metadata.Person("Roberto Gómez", "Gómez, Roberto"))
        self._metadata.authors.append(ebook_metadata.Person("Sancho Panza", "Panza, Sancho"))

        fileName = self._generateEbook()

        self.assertEqual(fileName, "AA. VV. - Titulo del libro (r1.0 Editor del libro).epub")

    def test_epub_file_name_when_one_author_and_simple_collection(self):
        self._metadata.title = "Título del libro"
        self._metadata.editor = "Editor del libro"
        self._metadata.authors.append(ebook_metadata.Person("Juan Pérez", "Pérez, Juan"))
        self._metadata.subCollectionName = "Esta es la serie"
        self._metadata.collectionVolume = "10"

        fileName = self._generateEbook()

        self.assertEqual(fileName, "Perez, Juan - [Esta es la serie 10] Titulo del libro (r1.0 Editor del libro).epub")

    def test_epub_file_name_when_one_author_and_subcollection(self):
        self._metadata.title = "Título del libro"
        self._metadata.editor = "Editor del libro"
        self._metadata.authors.append(ebook_metadata.Person("Juan Pérez", "Pérez, Juan"))
        self._metadata.collectionName = "Esta es la saga"
        self._metadata.subCollectionName = "Esta es la serie"
        self._metadata.collectionVolume = "10"

        fileName = self._generateEbook()

        self.assertEqual(fileName, "[Esta es la saga] [Esta es la serie 10] Perez, Juan - Titulo del "
                                   "libro (r1.0 Editor del libro).epub")

    def test_epub_file_name_when_two_authors_and_subcollection(self):
        self._metadata.title = "Título del libro"
        self._metadata.editor = "Editor del libro"
        self._metadata.authors.append(ebook_metadata.Person("Juan Pérez", "Pérez, Juan"))
        self._metadata.authors.append(ebook_metadata.Person("Roberto Gómez", "Gómez, Roberto"))
        self._metadata.collectionName = "Esta es la saga"
        self._metadata.subCollectionName = "Esta es la serie"
        self._metadata.collectionVolume = "10"

        fileName = self._generateEbook()

        self.assertEqual(fileName, "[Esta es la saga] [Esta es la serie 10] Perez, Juan & Gomez, Roberto - Titulo del "
                                   "libro (r1.0 Editor del libro).epub")

    def test_toc_without_notes(self):
        self._metadata.title = "Título del libro"

        self._generateEbook()

        titles = self._outputEpub.getTitles()
        self.assertEqual([t[0] for t in titles], ["Cubierta", "Título del libro", "Autor"])
        self.assertTrue(titles[0][1].endswith(epubbase_names.COVER_FILENAME))
        self.assertTrue(titles[1][1].endswith(epubbase_names.TITLE_FILENAME))
        self.assertTrue(titles[2][1].endswith(epubbase_names.AUTHOR_FILENAME))

    def test_toc_with_notes(self):
        self._metadata.title = "Título del libro"

        self._generateEbook([ebook_data.NotesSection()])

        titles = self._outputEpub.getTitles()
        self.assertEqual([t[0] for t in titles], ["Cubierta", "Título del libro", "Autor", "Notas"])
        self.assertTrue(titles[0][1].endswith(epubbase_names.COVER_FILENAME))
        self.assertTrue(titles[1][1].endswith(epubbase_names.TITLE_FILENAME))
        self.assertTrue(titles[2][1].endswith(epubbase_names.AUTHOR_FILENAME))
        self.assertTrue(titles[3][1].endswith(epubbase_names.NOTES_FILENAME))

    def test_default_images_exist(self):
        self._generateEbook()

        self.assertTrue(self._outputEpub.hasFile(epubbase_names.EPL_LOGO_FILENAME))
        self.assertTrue(self._outputEpub.hasFile(epubbase_names.AUTHOR_IMAGE_FILENAME))
        self.assertTrue(self._outputEpub.hasFile(epubbase_names.COVER_IMAGE_FILENAME))
        self.assertTrue(self._outputEpub.hasFile(epubbase_names.EX_LIBRIS_FILENAME))

    def test_custom_cover_image_and_author_image_exist(self):
        # Si bien estas dos variables deben contener una serie de bytes que representan
        # una imagen, para propósitos de testeo puedo usar simplemente un string.
        self._metadata.coverImage = "cover image"
        self._metadata.authorImage = "author image"

        self._generateEbook()

        coverImage = self._outputEpub.read(self._outputEpub.getFullPathToFile(epubbase_names.COVER_IMAGE_FILENAME))
        self.assertEqual(coverImage.decode(), "cover image")
        authorImage = self._outputEpub.read(self._outputEpub.getFullPathToFile(epubbase_names.AUTHOR_IMAGE_FILENAME))
        self.assertEqual(authorImage.decode(), "author image")

    def test_css_exists(self):
        self._generateEbook()

        self.assertTrue(self._outputEpub.hasFile(epubbase_names.STYLE_FILENAME))

    def test_ibooks_fonts_file_exists(self):
        self._generateEbook()

        self.assertTrue(self._outputEpub.hasFile(epubbase_names.IBOOKS_EMBEDDED_FONTS_FILENAME))

    def _generateEbook(self, sections=None):
        ebookData = ebook_data.EbookData()

        if sections:
            for section in sections:
                ebookData.addSection(section)

        eebook = ebook.Ebook(ebookData, self._metadata)
        fileName = eebook.save(self._outputFile)
        self._outputEpub = epub.EpubReader(self._outputFile)
        return fileName

    def _getInfoFile(self):
        try:
            return etree.XML(self._outputEpub.read("OEBPS/Text/{0}".format(epubbase_names.INFO_FILENAME)))
        except KeyError as e:
            self.fail(e)

    def _getTitleFile(self):
        try:
            return etree.XML(self._outputEpub.read("OEBPS/Text/{0}".format(epubbase_names.TITLE_FILENAME)))
        except KeyError as e:
            self.fail(e)

    def _getSynopsisFile(self):
        try:
            return etree.XML(self._outputEpub.read("OEBPS/Text/{0}".format(epubbase_names.SYNOPSIS_FILENAME)))
        except KeyError as e:
            self.fail(e)

    def _getDedicationFile(self):
        try:
            return etree.XML(self._outputEpub.read("OEBPS/Text/{0}".format(epubbase_names.DEDICATION_FILENAME)))
        except KeyError as e:
            self.fail(e)

    def _getAuthorFile(self):
        try:
            return etree.XML(self._outputEpub.read("OEBPS/Text/{0}".format(epubbase_names.AUTHOR_FILENAME)))
        except KeyError as e:
            self.fail(e)

    def _getCoverFile(self):
        try:
            return etree.XML(self._outputEpub.read("OEBPS/Text/{0}".format(epubbase_names.COVER_FILENAME)))
        except KeyError as e:
            self.fail(e)

    def _xpath(self, element, xpath):
        return element.xpath(xpath, namespaces=EbookTests._NAMESPACES)


if __name__ == "__main__":
    unittest.main()