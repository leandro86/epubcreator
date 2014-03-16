import unittest
import tempfile
import datetime
import re

from lxml import etree
from pyepub.pyepubreader import epub

from epubcreator import ebook, ebook_data, ebook_metadata, epubbase_names
from epubcreator.misc import utils


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

    def test_required_xhtml_files_exist(self):
        self._generateEbook()

        self.assertTrue(self._outputEpub.hasFile(epubbase_names.COVER_FILENAME))
        self.assertTrue(self._outputEpub.hasFile(epubbase_names.SYNOPSIS_FILENAME))
        self.assertTrue(self._outputEpub.hasFile(epubbase_names.TITLE_FILENAME))
        self.assertTrue(self._outputEpub.hasFile(epubbase_names.INFO_FILENAME))

    def test_required_images_exist(self):
        self._generateEbook()

        self.assertTrue(self._outputEpub.hasFile(epubbase_names.COVER_FILENAME))
        self.assertTrue(self._outputEpub.hasFile(epubbase_names.EPL_LOGO_FILENAME))
        self.assertTrue(self._outputEpub.hasFile(epubbase_names.EX_LIBRIS_FILENAME))

    def test_css_file_exists(self):
        self._generateEbook()

        self.assertTrue(self._outputEpub.hasFile(epubbase_names.STYLE_FILENAME))

    def test_ibooks_fonts_file_exists(self):
        self._generateEbook()

        self.assertTrue(self._outputEpub.hasFile(epubbase_names.IBOOKS_EMBEDDED_FONTS_FILENAME))

    def test_default_synopsis_text_in_synopsis_file(self):
        self._metadata.synopsis = ""

        self._generateEbook()

        synopsis = self._getSynopsisFile()

        self.assertEqual(self._xpath(synopsis, "count(//x:p)"), 2)

        gotSynopsis = "".join(self._xpath(synopsis, "x:body/x:div[@class = 'sinopsis']/x:p[1][@class = 'salto10']//text()"))
        gotSynopsis += "".join(self._xpath(synopsis, "x:body/x:div[@class = 'sinopsis']/x:p[2]//text()"))

        wantSynopsis = utils.removeTags(ebook_metadata.Metadata.DEFAULT_SYNOPSIS)

        self.assertEqual(gotSynopsis, wantSynopsis.replace("\n", ""))

    def test_synopsis_text_in_synopsis_file(self):
        self._metadata.synopsis = "Párrafo 1.\nPárrafo 2.\nPárrafo 3."

        self._generateEbook()

        synopsis = self._getSynopsisFile()

        self.assertEqual(self._xpath(synopsis, "count(//x:p)"), 3)

        self.assertEqual(self._xpath(synopsis, "x:body/x:div[@class = 'sinopsis']/x:p[1][@class = 'salto10']/text()")[0], "Párrafo 1.")
        self.assertEqual(self._xpath(synopsis, "x:body/x:div[@class = 'sinopsis']/x:p[2]/text()")[0], "Párrafo 2.")
        self.assertEqual(self._xpath(synopsis, "x:body/x:div[@class = 'sinopsis']/x:p[3]/text()")[0], "Párrafo 3.")

    def test_synopsis_text_with_tags_are_preserved_in_synopsis_file(self):
        self._metadata.synopsis = "Párrafo 1.\n<strong>Párrafo <em>2</em></strong>.\n<span>Párrafo 3.</span>"

        self._generateEbook()

        synopsis = self._getSynopsisFile()

        self.assertEqual(self._xpath(synopsis, "count(//x:p)"), 3)

        self.assertEqual(self._xpath(synopsis, "x:body/x:div[@class = 'sinopsis']/x:p[1][@class = 'salto10']/text()")[0], "Párrafo 1.")
        self.assertEqual(self._xpath(synopsis, "x:body/x:div[@class = 'sinopsis']/x:p[2]//text()"), ["Párrafo ", "2", "."])
        self.assertEqual(self._xpath(synopsis, "x:body/x:div[@class = 'sinopsis']/x:p[3]//text()"), ["Párrafo 3."])

    def test_synopsis_text_in_metadata(self):
        self._metadata.synopsis = "Párrafo 1.\nPárrafo 2.\nPárrafo 3."

        self._generateEbook()

        self.assertEqual(self._outputEpub.getDescription(), "Párrafo 1. Párrafo 2. Párrafo 3.")

    def test_synopsis_text_with_tags_are_stripped_in_metadata(self):
        self._metadata.synopsis = "Párrafo 1.\n<strong>Párrafo <em>2</em></strong>.\n<span>Párrafo 3.</span>"

        self._generateEbook()

        self.assertEqual(self._outputEpub.getDescription(), "Párrafo 1. Párrafo 2. Párrafo 3.")

    def test_default_author_in_title_file(self):
        self._metadata.authors.clear()

        self._generateEbook()

        title = self._getTitleFile()

        self.assertEqual(self._xpath(title, "x:body/x:p[@class = 'tautor']/text()")[0], ebook_metadata.Metadata.DEFAULT_AUTHOR)

    def test_single_author_in_title_file(self):
        self._metadata.authors.append(ebook_metadata.Person("Jorge Luis Borges", "bla"))

        self._generateEbook()

        title = self._getTitleFile()

        self.assertEqual(self._xpath(title, "x:body/x:p[@class = 'tautor']/text()")[0], "Jorge Luis Borges")

    def test_multiple_authors_in_title_file(self):
        self._metadata.authors.append(ebook_metadata.Person("Jorge Luis Borges", "bla"))
        self._metadata.authors.append(ebook_metadata.Person("Edgar Allan Poe", "bla"))
        self._metadata.authors.append(ebook_metadata.Person("William Shakespeare", "bla"))
        self._metadata.authors.append(ebook_metadata.Person("H. P. Lovecraft", "bla"))

        self._generateEbook()

        title = self._getTitleFile()

        self.assertEqual(self._xpath(title, "x:body/x:p[@class = 'tautor']/text()")[0],
                         "Jorge Luis Borges & Edgar Allan Poe & William Shakespeare & H. P. Lovecraft")

    def test_default_author_in_metadata(self):
        self._metadata.authors.clear()

        self._generateEbook()

        authors = self._outputEpub.getAuthors()
        self.assertEqual(len(authors), 1)
        self.assertEqual(authors[0], (ebook_metadata.Metadata.DEFAULT_AUTHOR, ebook_metadata.Metadata.DEFAULT_AUTHOR))

    def test_single_author_in_metadata(self):
        self._metadata.authors.append(ebook_metadata.Person("Jorge Luis Borges", "Borges, Jorge Luis"))

        self._generateEbook()

        authors = self._outputEpub.getAuthors()
        self.assertEqual(len(authors), 1)
        self.assertEqual(authors[0], ("Jorge Luis Borges", "Borges, Jorge Luis"))

    def test_multiple_authors_in_metadata(self):
        self._metadata.authors.append(ebook_metadata.Person("Jorge Luis Borges", "Borges, Jorge Luis"))
        self._metadata.authors.append(ebook_metadata.Person("Edgar Allan Poe", "Poe, Edgar Allan"))
        self._metadata.authors.append(ebook_metadata.Person("William Shakespeare", "Shakespeare, William"))
        self._metadata.authors.append(ebook_metadata.Person("H. P. Lovecraft", "Lovecraft, H. P."))

        self._generateEbook()

        authors = self._outputEpub.getAuthors()
        self.assertEqual(len(authors), 1)
        self.assertEqual(authors[0], ("Jorge Luis Borges & Edgar Allan Poe & William Shakespeare & H. P. Lovecraft",
                                      "Borges, Jorge Luis & Poe, Edgar Allan & Shakespeare, William & Lovecraft, H. P."))

    def test_default_title_in_title_file(self):
        self._metadata.title = ""

        self._generateEbook()

        title = self._getTitleFile()

        self.assertEqual(self._xpath(title, "x:body/x:h1[@class = 'ttitulo']/text()")[0], ebook_metadata.Metadata.DEFAULT_TITLE)

    def test_title_in_title_file(self):
        self._metadata.title = "Título del libro"

        self._generateEbook()

        title = self._getTitleFile()

        self.assertEqual(self._xpath(title, "x:body/x:h1[@class = 'ttitulo']/text()")[0], "Título del libro")

    def test_default_title_in_title_metadata(self):
        self._metadata.title = ""

        self._generateEbook()

        self.assertEqual(self._outputEpub.getTitle(), ebook_metadata.Metadata.DEFAULT_TITLE)

    def test_title_in_title_metadata(self):
        self._metadata.title = "Título del libro"

        self._generateEbook()

        self.assertEqual(self._outputEpub.getTitle(), "Título del libro")

    def test_subtitle_in_title_file(self):
        self._metadata.subtitle = "Subtítulo del libro"

        self._generateEbook()

        title = self._getTitleFile()

        self.assertEqual(self._xpath(title, "x:body/x:p[@class = 'tsubtitulo']/text()")[0], "Subtítulo del libro")

    def test_not_subtitle_in_title_file(self):
        self._metadata.subtitle = ""

        self._generateEbook()

        title = self._getTitleFile()

        self.assertFalse(self._xpath(title, "x:body/x:p[@class = 'tsubtitulo']/text()"))
        # En titulo.xhtml hay un comentario indicando en el campo de subtítulo que es opcional, por eso debo verificar
        # que también ese comentario se haya borrado.
        self.assertFalse(self._xpath(title, "x:body/comment()"))

    def test_revision_in_title_file(self):
        self._generateEbook()

        title = self._getTitleFile()

        self.assertEqual(self._xpath(title, "x:body/x:p[@class = 'trevision']/text()")[0], "ePub r1.0")

    def test_default_editor_in_title_file(self):
        self._metadata.editor = ""

        self._generateEbook()

        title = self._getTitleFile()

        self.assertEqual(self._xpath(title, "x:body/x:p[@class = 'tfirma']/text()")[0], ebook_metadata.Metadata.DEFAULT_EDITOR + " ")

    def test_editor_in_title_file(self):
        self._metadata.editor = "El editor"

        self._generateEbook()

        title = self._getTitleFile()

        self.assertEqual(self._xpath(title, "x:body/x:p[@class = 'tfirma']/text()")[0], "El editor ")

    def test_modification_date_in_title_file(self):
        self._generateEbook()

        title = self._getTitleFile()

        self.assertEqual(self._xpath(title, "x:body/x:p[@class = 'tfirma']/x:span[@class = 'tfecha']/text()")[0],
                         datetime.datetime.now().strftime("%d.%m.%y"))

    def test_modification_date_in_metadata(self):
        self._generateEbook()

        self.assertEqual(self._outputEpub.getModificationDate(), datetime.datetime.now().strftime("%Y-%m-%d"))

    def test_original_title_in_info_file(self):
        self._metadata.originalTitle = "El título original"

        self._generateEbook()

        info = self._getInfoFile()

        # El título en el campo "Título original" se encuentra dentro de un tag "em".
        self.assertEqual(self._xpath(info, "x:body/x:div[@class = 'info']/x:p[1]//text()"), ["Título original: ", "El título original"])

    def test_not_original_title_in_info_file(self):
        self._metadata.originalTitle = ""

        self._generateEbook()

        info = self._getInfoFile()

        # El título en el campo "Título original" se encuentra dentro de un tag "em".
        self.assertFalse(self._xpath(info, "x:body/x:div[@class = 'info']/x:p[starts-with(text(), 'Título original')]"))

    def test_default_author_in_info_file(self):
        self._metadata.authors.clear()

        self._generateEbook()

        info = self._getInfoFile()

        self.assertEqual(self._xpath(info, "x:body/x:div[@class = 'info']/x:p[1]/text()")[0], ebook_metadata.Metadata.DEFAULT_AUTHOR)

    def test_single_author_in_info_file(self):
        self._metadata.authors.append(ebook_metadata.Person("Jorge Luis Borges", "bla"))

        self._generateEbook()

        info = self._getInfoFile()

        self.assertEqual(self._xpath(info, "x:body/x:div[@class = 'info']/x:p[1]/text()")[0], "Jorge Luis Borges")

    def test_multiple_authors_in_info_file(self):
        self._metadata.authors.append(ebook_metadata.Person("Jorge Luis Borges", "bla"))
        self._metadata.authors.append(ebook_metadata.Person("Edgar Allan Poe", "bla"))
        self._metadata.authors.append(ebook_metadata.Person("William Shakespeare", "bla"))
        self._metadata.authors.append(ebook_metadata.Person("H. P. Lovecraft", "bla"))

        self._generateEbook()

        info = self._getInfoFile()

        self.assertEqual(self._xpath(info, "x:body/x:div[@class = 'info']/x:p[1]/text()")[0],
                         "Jorge Luis Borges & Edgar Allan Poe & William Shakespeare & H. P. Lovecraft")

    def test_publication_date_in_info_file(self):
        self._metadata.publicationDate = datetime.date(1756, 5, 9)

        self._generateEbook()

        info = self._getInfoFile()

        # Antes de la coma viene el nombre del autor, que siempre va a estar.
        self.assertTrue(self._xpath(info, "x:body/x:div[@class = 'info']/x:p[1]/text()")[0].endswith(", 1756"))

    def test_not_publication_date_in_info_file(self):
        self._metadata.publicationDate = None

        self._generateEbook()

        info = self._getInfoFile()

        # La fecha de publicación en el idioma original se coloca en el mismo párrafo, junto con el
        # autor, y separada por una coma.
        self.assertFalse("," in self._xpath(info, "x:body/x:div[@class = 'info']/x:p[1]/text()")[0])

    def test_publication_date_in_metadata(self):
        self._metadata.publicationDate = datetime.date(1756, 5, 9)

        self._generateEbook()

        self.assertEqual(self._outputEpub.getPublicationDate(), "1756-05-09")

    def test_not_publication_date_in_metadata(self):
        self._metadata.publicationDate = None

        self._generateEbook()

        self.assertIsNone(self._outputEpub.getPublicationDate())

    def test_single_translator_in_info_file(self):
        self._metadata.translators.append(ebook_metadata.Person("Jorge Luis Borges", "bla"))

        self._generateEbook()

        info = self._getInfoFile()

        self.assertEqual(self._xpath(info, "x:body/x:div[@class = 'info']/x:p[2]/text()")[0], "Traducción: Jorge Luis Borges")

    def test_multiple_translators_in_info_file(self):
        self._metadata.translators.append(ebook_metadata.Person("Jorge Luis Borges", "bla"))
        self._metadata.translators.append(ebook_metadata.Person("Edgar Allan Poe", "bla"))
        self._metadata.translators.append(ebook_metadata.Person("William Shakespeare", "bla"))
        self._metadata.translators.append(ebook_metadata.Person("H. P. Lovecraft", "bla"))

        self._generateEbook()

        info = self._getInfoFile()

        self.assertEqual(self._xpath(info, "x:body/x:div[@class = 'info']/x:p[2]/text()")[0],
                         "Traducción: Jorge Luis Borges & Edgar Allan Poe & William Shakespeare & H. P. Lovecraft")

    def test_not_translator_in_info_file(self):
        self._metadata.translators.clear()

        self._generateEbook()

        info = self._getInfoFile()

        self.assertFalse(self._xpath(info, "x:body/x:div[@class = 'info']/x:p[starts-with(text(), 'Traducción')]"))

    def test_single_translator_in_metadata(self):
        self._metadata.translators.append(ebook_metadata.Person("Jorge Luis Borges", "Borges, Jorge Luis"))

        self._generateEbook()

        translators = self._outputEpub.getTranslators()
        self.assertEqual(len(translators), 1)
        self.assertEqual(translators[0], ("Jorge Luis Borges", "Borges, Jorge Luis"))

    def test_multiple_translators_in_metadata(self):
        self._metadata.translators.append(ebook_metadata.Person("Jorge Luis Borges", "Borges, Jorge Luis"))
        self._metadata.translators.append(ebook_metadata.Person("Edgar Allan Poe", "Poe, Edgar Allan"))
        self._metadata.translators.append(ebook_metadata.Person("William Shakespeare", "Shakespeare, William"))
        self._metadata.translators.append(ebook_metadata.Person("H. P. Lovecraft", "Lovecraft, H. P."))

        self._generateEbook()

        translators = self._outputEpub.getTranslators()
        self.assertEqual(len(translators), 1)
        self.assertEqual(translators[0], ("Jorge Luis Borges & Edgar Allan Poe & William Shakespeare & H. P. Lovecraft",
                                          "Borges, Jorge Luis & Poe, Edgar Allan & Shakespeare, William & Lovecraft, H. P."))

    def test_not_translator_in_metadata(self):
        self._metadata.translators.clear()

        self._generateEbook()

        self.assertFalse(self._outputEpub.getTranslators())

    def test_single_ilustrator_in_info_file(self):
        self._metadata.ilustrators.append(ebook_metadata.Person("Jorge Luis Borges", "bla"))

        self._generateEbook()

        info = self._getInfoFile()

        self.assertEqual(self._xpath(info, "x:body/x:div[@class = 'info']/x:p[2]/text()")[0], "Ilustraciones: Jorge Luis Borges")

    def test_multiple_ilustrators_in_info_file(self):
        self._metadata.ilustrators.append(ebook_metadata.Person("Jorge Luis Borges", "bla"))
        self._metadata.ilustrators.append(ebook_metadata.Person("Edgar Allan Poe", "bla"))
        self._metadata.ilustrators.append(ebook_metadata.Person("William Shakespeare", "bla"))
        self._metadata.ilustrators.append(ebook_metadata.Person("H. P. Lovecraft", "bla"))

        self._generateEbook()

        info = self._getInfoFile()

        self.assertEqual(self._xpath(info, "x:body/x:div[@class = 'info']/x:p[2]/text()")[0],
                         "Ilustraciones: Jorge Luis Borges & Edgar Allan Poe & William Shakespeare & H. P. Lovecraft")

    def test_not_ilustrator_in_info_file(self):
        self._metadata.ilustrators.clear()

        self._generateEbook()

        info = self._getInfoFile()

        self.assertFalse(self._xpath(info, "x:body/x:div[@class = 'info']/x:p[starts-with(text(), 'Ilustraciones')]"))

    def test_single_ilustrator_in_metadata(self):
        self._metadata.ilustrators.append(ebook_metadata.Person("Jorge Luis Borges", "Borges, Jorge Luis"))

        self._generateEbook()

        ilustrators = self._outputEpub.getIlustrators()
        self.assertEqual(len(ilustrators), 1)
        self.assertEqual(ilustrators[0], ("Jorge Luis Borges", "Borges, Jorge Luis"))

    def test_multiple_ilustrators_in_metadata(self):
        self._metadata.ilustrators.append(ebook_metadata.Person("Jorge Luis Borges", "Borges, Jorge Luis"))
        self._metadata.ilustrators.append(ebook_metadata.Person("Edgar Allan Poe", "Poe, Edgar Allan"))
        self._metadata.ilustrators.append(ebook_metadata.Person("William Shakespeare", "Shakespeare, William"))
        self._metadata.ilustrators.append(ebook_metadata.Person("H. P. Lovecraft", "Lovecraft, H. P."))

        self._generateEbook()

        ilustrators = self._outputEpub.getIlustrators()
        self.assertEqual(len(ilustrators), 1)
        self.assertEqual(ilustrators[0], ("Jorge Luis Borges & Edgar Allan Poe & William Shakespeare & H. P. Lovecraft",
                                          "Borges, Jorge Luis & Poe, Edgar Allan & Shakespeare, William & Lovecraft, H. P."))

    def test_not_ilustrator_in_metadata(self):
        self._metadata.ilustrators.clear()

        self._generateEbook()

        self.assertFalse(self._outputEpub.getIlustrators())

    def test_default_cover_modification_in_info_file(self):
        self._metadata.coverModification = ""

        self._generateEbook()

        info = self._getInfoFile()

        self.assertTrue(self._xpath(info, "x:body/x:div[@class = 'info']/x:p[2]/text()")[0].
                        startswith("{0} de cubierta: ".format(ebook_metadata.Metadata.DEFAULT_COVER_MODIFICATION)))

    def test_default_cover_designer_in_info_file(self):
        self._metadata.coverDesigner = ""

        self._generateEbook()

        info = self._getInfoFile()

        self.assertTrue(self._xpath(info, "x:body/x:div[@class = 'info']/x:p[2]/text()")[0].endswith(ebook_metadata.Metadata.DEFAULT_EDITOR))

    def test_cover_modification_in_info_file(self):
        self._metadata.coverModification = "Retoque"

        self._generateEbook()

        info = self._getInfoFile()

        self.assertTrue(self._xpath(info, "x:body/x:div[@class = 'info']/x:p[2]/text()")[0].startswith("Retoque de cubierta: "))

    def test_cover_designer_in_info_file(self):
        self._metadata.coverDesigner = "Jorge Luis Borges"

        self._generateEbook()

        info = self._getInfoFile()

        self.assertTrue(self._xpath(info, "x:body/x:div[@class = 'info']/x:p[2]/text()")[0].endswith("Jorge Luis Borges"))

    def test_default_editor_in_info_file(self):
        self._metadata.editor = ""

        self._generateEbook()

        info = self._getInfoFile()

        self.assertEqual(self._xpath(info, "x:body/x:div[@class = 'info']/x:p[3]/text()")[0],
                         "Editor digital: {0}".format(ebook_metadata.Metadata.DEFAULT_EDITOR))

    def test_editor_in_info_file(self):
        self._metadata.editor = "El editor"

        self._generateEbook()

        info = self._getInfoFile()

        self.assertEqual(self._xpath(info, "x:body/x:div[@class = 'info']/x:p[3]/text()")[0], "Editor digital: El editor")

    def test_epub_base_revision_in_info_file(self):
        self._generateEbook()

        info = self._getInfoFile()

        self.assertEqual(self._xpath(info, "x:body/x:div[@class = 'info']/x:p[4]/text()")[0], "ePub base r1.1")

    def test_default_dedication_text_in_dedication_file(self):
        self._metadata.dedication = ""

        self._generateEbook()

        dedication = self._getDedicationFile()

        self.assertEqual(self._xpath(dedication, "count(//x:p)"), 2)

        gotDedication = "".join(self._xpath(dedication, "x:body/x:div[@class = 'dedicatoria']/x:p[1]//text()"))
        gotDedication += "".join(self._xpath(dedication, "x:body/x:div[@class = 'dedicatoria']/x:p[2][@class = 'salto05']//text()"))

        wantDedication = utils.removeTags(ebook_metadata.Metadata.DEFAULT_DEDICATION)

        self.assertEqual(gotDedication, wantDedication.replace("\n", ""))

    def test_dedication_text_in_dedication_file(self):
        self._metadata.dedication = "Párrafo 1.\nPárrafo 2.\nPárrafo 3."

        self._generateEbook()

        dedication = self._getDedicationFile()

        self.assertEqual(self._xpath(dedication, "count(//x:p)"), 3)

        self.assertEqual(self._xpath(dedication, "x:body/x:div[@class = 'dedicatoria']/x:p[1]/text()")[0], "Párrafo 1.")
        self.assertEqual(self._xpath(dedication, "x:body/x:div[@class = 'dedicatoria']/x:p[2]/text()")[0], "Párrafo 2.")
        self.assertEqual(self._xpath(dedication, "x:body/x:div[@class = 'dedicatoria']/x:p[3]/text()")[0], "Párrafo 3.")

    def test_dedication_text_with_tags_are_preserved_in_dedication_file(self):
        self._metadata.dedication = "Párrafo 1.\n<strong>Párrafo <em>2</em></strong>.\n<span>Párrafo 3.</span>"

        self._generateEbook()

        dedication = self._getDedicationFile()

        self.assertEqual(self._xpath(dedication, "count(//x:p)"), 3)

        self.assertEqual(self._xpath(dedication, "x:body/x:div[@class = 'dedicatoria']/x:p[1]/text()")[0], "Párrafo 1.")
        self.assertEqual(self._xpath(dedication, "x:body/x:div[@class = 'dedicatoria']/x:p[2]//text()"), ["Párrafo ", "2", "."])
        self.assertEqual(self._xpath(dedication, "x:body/x:div[@class = 'dedicatoria']/x:p[3]//text()"), ["Párrafo 3."])

    def test_default_author_biography_text_in_author_file(self):
        self._metadata.authorBiography = ""

        self._generateEbook()

        author = self._getAuthorFile()

        self.assertEqual(self._xpath(author, "count(//x:p)"), 2)

        gotAuthorBiography = "".join(self._xpath(author, "x:body/x:div[@class = 'autor']/x:p[1]//text()"))
        gotAuthorBiography += "".join(self._xpath(author, "x:body/x:div[@class = 'autor']/x:p[2]//text()"))

        wantAuthorBiography = utils.removeTags(ebook_metadata.Metadata.DEFAULT_AUTHOR_BIOGRAPHY)

        self.assertEqual(gotAuthorBiography, wantAuthorBiography.replace("\n", ""))

    def test_author_biography_text_in_author_file(self):
        self._metadata.authorBiography = "Párrafo 1.\nPárrafo 2.\nPárrafo 3."

        self._generateEbook()

        author = self._getAuthorFile()

        self.assertEqual(self._xpath(author, "/x:html/x:body/x:div[@class = 'autor']/x:p[position() = 1]/text()")[0], "Párrafo 1.")
        self.assertEqual(self._xpath(author, "/x:html/x:body/x:div[@class = 'autor']/x:p[position() = 2]/text()")[0], "Párrafo 2.")
        self.assertEqual(self._xpath(author, "/x:html/x:body/x:div[@class = 'autor']/x:p[position() = 3]/text()")[0], "Párrafo 3.")

    def test_author_biography_text_with_tags_are_preserved_in_author_file(self):
        self._metadata.authorBiography = "Párrafo 1.\n<strong>Párrafo <em>2</em></strong>.\n<span>Párrafo 3.</span>"

        self._generateEbook()

        author = self._getAuthorFile()

        self.assertEqual(self._xpath(author, "count(//x:p)"), 3)

        self.assertEqual(self._xpath(author, "x:body/x:div[@class = 'autor']/x:p[1]/text()")[0], "Párrafo 1.")
        self.assertEqual(self._xpath(author, "x:body/x:div[@class = 'autor']/x:p[2]//text()"), ["Párrafo ", "2", "."])
        self.assertEqual(self._xpath(author, "x:body/x:div[@class = 'autor']/x:p[3]//text()"), ["Párrafo 3."])

    def test_author_image_exists(self):
        self._generateEbook()

        self.assertTrue(self._outputEpub.hasFile(epubbase_names.AUTHOR_IMAGE_FILENAME))

    def test_author_file_is_last_in_play_order_when_epub_not_has_notes(self):
        self._generateEbook()

        htmlFiles = self._outputEpub.getHtmlFileNamesReadingOrder()
        self.assertEqual(htmlFiles[-1], epubbase_names.AUTHOR_FILENAME)

    def test_author_file_is_second_to_last_in_play_order_when_epub_contains_notes(self):
        self._generateEbook([ebook_data.NotesSection()])

        htmlFiles = self._outputEpub.getHtmlFileNamesReadingOrder()
        self.assertEqual(htmlFiles[-2], epubbase_names.AUTHOR_FILENAME)

    def test_required_entries_in_toc(self):
        self._generateEbook()

        titles = self._outputEpub.getTitles()

        self.assertEqual([t[0] for t in titles], ["Cubierta", ebook_metadata.Metadata.DEFAULT_TITLE, "Autor"])
        self.assertTrue(titles[0][1].endswith(epubbase_names.COVER_FILENAME))
        self.assertTrue(titles[1][1].endswith(epubbase_names.TITLE_FILENAME))
        self.assertTrue(titles[2][1].endswith(epubbase_names.AUTHOR_FILENAME))

    def test_notes_entry_exists_in_toc_when_epub_contains_notes(self):
        self._generateEbook([ebook_data.NotesSection()])

        titles = self._outputEpub.getTitles()

        self.assertEqual(titles[-1][0], "Notas")
        self.assertTrue(titles[-1][1].endswith(epubbase_names.NOTES_FILENAME))

    def test_title_entry_in_toc(self):
        self._metadata.title = "El título del libro"

        self._generateEbook()

        titles = self._outputEpub.getTitles()

        self.assertEqual(titles[1][0], "El título del libro")
        self.assertTrue(titles[1][1].endswith(epubbase_names.TITLE_FILENAME))

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

    def test_epub_file_name_default_metadata(self):
        fileName = self._generateEbook()

        defaultAuthor = utils.removeSpecialCharacters(ebook_metadata.Metadata.DEFAULT_AUTHOR)
        defaultTitle = utils.removeSpecialCharacters(ebook_metadata.Metadata.DEFAULT_TITLE)
        defaultEditor = utils.removeSpecialCharacters(ebook_metadata.Metadata.DEFAULT_EDITOR)
        defaultBookId = ebook_metadata.Metadata.DEFAULT_BOOK_ID

        self.assertEqual(fileName, "{0} - {1} [{2}] (r1.0 {3}).epub".format(defaultAuthor, defaultTitle, defaultBookId, defaultEditor))

    def test_epub_file_name_when_one_author_and_no_collection(self):
        self._metadata.authors.append(ebook_metadata.Person("bla", "Borges, Jorge Luis"))

        fileName = self._generateEbook()

        defaultTitle = utils.removeSpecialCharacters(ebook_metadata.Metadata.DEFAULT_TITLE)
        defaultEditor = utils.removeSpecialCharacters(ebook_metadata.Metadata.DEFAULT_EDITOR)
        defaultBookId = ebook_metadata.Metadata.DEFAULT_BOOK_ID

        self.assertEqual(fileName, "Borges, Jorge Luis - {0} [{1}] (r1.0 {2}).epub".format(defaultTitle, defaultBookId, defaultEditor))

    def test_epub_file_name_when_two_authors_and_no_collection(self):
        self._metadata.authors.append(ebook_metadata.Person("bla", "Borges, Jorge Luis"))
        self._metadata.authors.append(ebook_metadata.Person("bla", "Shakespeare, William"))

        fileName = self._generateEbook()

        defaultTitle = utils.removeSpecialCharacters(ebook_metadata.Metadata.DEFAULT_TITLE)
        defaultEditor = utils.removeSpecialCharacters(ebook_metadata.Metadata.DEFAULT_EDITOR)
        defaultBookId = ebook_metadata.Metadata.DEFAULT_BOOK_ID

        self.assertEqual(fileName, "Borges, Jorge Luis & Shakespeare, William - {0} [{1}] (r1.0 {2}).epub".format(defaultTitle,
                                                                                                                  defaultBookId,
                                                                                                                  defaultEditor))

    def test_epub_file_name_when_three_authors_and_no_collection(self):
        self._metadata.authors.append(ebook_metadata.Person("bla", "bla"))
        self._metadata.authors.append(ebook_metadata.Person("bla", "bla"))
        self._metadata.authors.append(ebook_metadata.Person("bla", "bla"))

        fileName = self._generateEbook()

        defaultTitle = utils.removeSpecialCharacters(ebook_metadata.Metadata.DEFAULT_TITLE)
        defaultEditor = utils.removeSpecialCharacters(ebook_metadata.Metadata.DEFAULT_EDITOR)
        defaultBookId = ebook_metadata.Metadata.DEFAULT_BOOK_ID

        self.assertEqual(fileName, "AA. VV. - {0} [{1}] (r1.0 {2}).epub".format(defaultTitle, defaultBookId, defaultEditor))

    def test_epub_file_name_when_one_author_and_simple_collection(self):
        self._metadata.authors.append(ebook_metadata.Person("bla", "Borges, Jorge Luis"))
        self._metadata.subCollectionName = "Esta es la serie"
        self._metadata.collectionVolume = "10"

        fileName = self._generateEbook()

        defaultTitle = utils.removeSpecialCharacters(ebook_metadata.Metadata.DEFAULT_TITLE)
        defaultEditor = utils.removeSpecialCharacters(ebook_metadata.Metadata.DEFAULT_EDITOR)
        defaultBookId = ebook_metadata.Metadata.DEFAULT_BOOK_ID

        self.assertEqual(fileName, "Borges, Jorge Luis - [Esta es la serie 10] {0} [{1}] (r1.0 {2}).epub".format(defaultTitle,
                                                                                                                 defaultBookId,
                                                                                                                 defaultEditor))

    def test_epub_file_name_when_one_author_and_subcollection(self):
        self._metadata.authors.append(ebook_metadata.Person("bla", "Borges, Jorge Luis"))
        self._metadata.collectionName = "Esta es la saga"
        self._metadata.subCollectionName = "Esta es la serie"
        self._metadata.collectionVolume = "10"

        fileName = self._generateEbook()

        defaultTitle = utils.removeSpecialCharacters(ebook_metadata.Metadata.DEFAULT_TITLE)
        defaultEditor = utils.removeSpecialCharacters(ebook_metadata.Metadata.DEFAULT_EDITOR)
        defaultBookId = ebook_metadata.Metadata.DEFAULT_BOOK_ID

        self.assertEqual(fileName,
                         "[Esta es la saga] [Esta es la serie 10] Borges, Jorge Luis - {0} [{1}] (r1.0 {2}).epub".format(defaultTitle,
                                                                                                                         defaultBookId,
                                                                                                                         defaultEditor))

    def test_epub_file_name_when_two_authors_and_subcollection(self):
        self._metadata.authors.append(ebook_metadata.Person("bla", "Borges, Jorge Luis"))
        self._metadata.authors.append(ebook_metadata.Person("bla", "Shakespeare, William"))
        self._metadata.collectionName = "Esta es la saga"
        self._metadata.subCollectionName = "Esta es la serie"
        self._metadata.collectionVolume = "10"

        fileName = self._generateEbook()

        defaultTitle = utils.removeSpecialCharacters(ebook_metadata.Metadata.DEFAULT_TITLE)
        defaultEditor = utils.removeSpecialCharacters(ebook_metadata.Metadata.DEFAULT_EDITOR)
        defaultBookId = ebook_metadata.Metadata.DEFAULT_BOOK_ID

        self.assertEqual(fileName,
                         "[Esta es la saga] [Esta es la serie 10] Borges, Jorge Luis & "
                         "Shakespeare, William - {0} [{1}] (r1.0 {2}).epub".format(defaultTitle, defaultBookId, defaultEditor))

    def test_epub_file_name_when_three_authors_and_subcollection(self):
        self._metadata.authors.append(ebook_metadata.Person("bla", "bla"))
        self._metadata.authors.append(ebook_metadata.Person("bla", "bla"))
        self._metadata.authors.append(ebook_metadata.Person("bla", "bla"))
        self._metadata.collectionName = "Esta es la saga"
        self._metadata.subCollectionName = "Esta es la serie"
        self._metadata.collectionVolume = "10"

        fileName = self._generateEbook()

        defaultTitle = utils.removeSpecialCharacters(ebook_metadata.Metadata.DEFAULT_TITLE)
        defaultEditor = utils.removeSpecialCharacters(ebook_metadata.Metadata.DEFAULT_EDITOR)
        defaultBookId = ebook_metadata.Metadata.DEFAULT_BOOK_ID

        self.assertEqual(fileName, "[Esta es la saga] [Esta es la serie 10] AA. VV. - {0} [{1}] (r1.0 {2}).epub".format(defaultTitle,
                                                                                                                        defaultBookId,
                                                                                                                        defaultEditor))

    def test_epub_file_name_bookid(self):
        self._metadata.authors.append(ebook_metadata.Person("Autor", "Autor"))
        self._metadata.bookId = "1234"

        fileName = self._generateEbook()

        defaultAuthor = utils.removeSpecialCharacters(ebook_metadata.Metadata.DEFAULT_AUTHOR)
        defaultTitle = utils.removeSpecialCharacters(ebook_metadata.Metadata.DEFAULT_TITLE)
        defaultEditor = utils.removeSpecialCharacters(ebook_metadata.Metadata.DEFAULT_EDITOR)

        self.assertEqual(fileName, "{0} - {1} [{2}] (r1.0 {3}).epub".format(defaultAuthor, defaultTitle, "1234", defaultEditor))

    def test_epub_file_name_title(self):
        self._metadata.title = "Este es el título"

        fileName = self._generateEbook()

        defaultAuthor = utils.removeSpecialCharacters(ebook_metadata.Metadata.DEFAULT_AUTHOR)
        defaultEditor = utils.removeSpecialCharacters(ebook_metadata.Metadata.DEFAULT_EDITOR)
        defaultBookId = ebook_metadata.Metadata.DEFAULT_BOOK_ID

        self.assertEqual(fileName, "{0} - Este es el titulo [{1}] (r1.0 {2}).epub".format(defaultAuthor, defaultBookId, defaultEditor))

    def test_epub_file_name_editor(self):
        self._metadata.editor = "Este es el editor"

        fileName = self._generateEbook()

        defaultAuthor = utils.removeSpecialCharacters(ebook_metadata.Metadata.DEFAULT_AUTHOR)
        defaultTitle = utils.removeSpecialCharacters(ebook_metadata.Metadata.DEFAULT_TITLE)
        defaultBookId = ebook_metadata.Metadata.DEFAULT_BOOK_ID

        self.assertEqual(fileName, "{0} - {1} [{2}] (r1.0 Este es el editor).epub".format(defaultAuthor, defaultTitle, defaultBookId))

    def test_epub_file_name_when_special_characters(self):
        self._metadata.title = "Títúló dél libro"
        self._metadata.authors.append(ebook_metadata.Person("bla", "Éste es el áutór"))
        self._metadata.editor = "Esté es él edítór"
        self._metadata.collectionName = "Esta es la ságá"
        self._metadata.subCollectionName = "Éstá es la série"
        self._metadata.collectionVolume = "10"

        fileName = self._generateEbook()

        defaultBookId = ebook_metadata.Metadata.DEFAULT_BOOK_ID

        self.assertEqual(fileName, "[Esta es la saga] [Esta es la serie 10] Este es el autor - "
                                   "Titulo del libro [{0}] (r1.0 Este es el editor).epub".format(defaultBookId))

    def test_cover_image(self):
        self._metadata.coverImage = "cover image"

        self._generateEbook()

        coverImage = self._outputEpub.read(self._outputEpub.getFullPathToFile(epubbase_names.COVER_IMAGE_FILENAME))
        self.assertEqual(coverImage.decode(), "cover image")

    def test_author_image(self):
        self._metadata.authorImage = "author image"

        self._generateEbook()

        authorImage = self._outputEpub.read(self._outputEpub.getFullPathToFile(epubbase_names.AUTHOR_IMAGE_FILENAME))
        self.assertEqual(authorImage.decode(), "author image")

    def test_default_language_in_metadata(self):
        self._metadata.language = ""

        self._generateEbook()

        self.assertTrue(self._outputEpub.getLanguage(), "es")

    def test_language_in_metadata(self):
        self._metadata.language = "en"

        self._generateEbook()

        self.assertTrue(self._outputEpub.getLanguage(), "en")

    def test_one_genretype_one_genre_one_subgenre_in_metadata(self):
        self._metadata.genres.append(ebook_metadata.Genre("Tipo1", "Genero1", "Subgenero1"))

        self._generateEbook()

        self.assertEqual(self._outputEpub.getSubject(), "Genero1, Subgenero1")

    def test_one_genretype_one_genre_two_subgenres_in_metadata(self):
        self._metadata.genres.append(ebook_metadata.Genre("Tipo1", "Genero1", "Subgenero1"))
        self._metadata.genres.append(ebook_metadata.Genre("Tipo1", "Genero1", "Subgenero2"))

        self._generateEbook()

        self.assertEqual(self._outputEpub.getSubject(), "Genero1, Subgenero1, Subgenero2")

    def test_one_genretype_two_genres_one_subgenre_in_metadata(self):
        self._metadata.genres.append(ebook_metadata.Genre("Tipo1", "Genero1", "Subgenero1"))
        self._metadata.genres.append(ebook_metadata.Genre("Tipo1", "Genero2", "Subgenero1"))

        self._generateEbook()

        self.assertEqual(self._outputEpub.getSubject(), "Genero1, Subgenero1, Genero2, Subgenero1")

    def test_one_genretype_two_genres_two_subgenres_in_metadata(self):
        self._metadata.genres.append(ebook_metadata.Genre("Tipo1", "Genero1", "Subgenero1"))
        self._metadata.genres.append(ebook_metadata.Genre("Tipo1", "Genero1", "Subgenero2"))
        self._metadata.genres.append(ebook_metadata.Genre("Tipo1", "Genero2", "Subgenero1"))
        self._metadata.genres.append(ebook_metadata.Genre("Tipo1", "Genero2", "Subgenero2"))

        self._generateEbook()

        self.assertEqual(self._outputEpub.getSubject(), "Genero1, Subgenero1, Subgenero2, Genero2, Subgenero1, Subgenero2")

    def test_genretype_not_get_saved_in_metadata(self):
        self._metadata.genres.append(ebook_metadata.Genre("Tipo1", "Genero1", "Subgenero1"))
        self._metadata.genres.append(ebook_metadata.Genre("Tipo1", "Genero1", "Subgenero2"))
        self._metadata.genres.append(ebook_metadata.Genre("Tipo2", "Genero2", "Subgenero1"))
        self._metadata.genres.append(ebook_metadata.Genre("Tipo2", "Genero2", "Subgenero2"))

        self._generateEbook()

        self.assertEqual(self._outputEpub.getSubject(), "Genero1, Subgenero1, Subgenero2, Genero2, Subgenero1, Subgenero2")

    def test_genres_are_sorted_in_metadata(self):
        self._metadata.genres.append(ebook_metadata.Genre("Tipo1", "d", "f"))
        self._metadata.genres.append(ebook_metadata.Genre("Tipo1", "k", "a"))
        self._metadata.genres.append(ebook_metadata.Genre("Tipo1", "a", "b"))
        self._metadata.genres.append(ebook_metadata.Genre("Tipo1", "u", "a"))
        self._metadata.genres.append(ebook_metadata.Genre("Tipo1", "a", "a"))
        self._metadata.genres.append(ebook_metadata.Genre("Tipo1", "d", "e"))

        self._generateEbook()

        self.assertEqual(self._outputEpub.getSubject(), "a, a, b, d, e, f, k, a, u, a")

    def test_not_genres_in_metadata(self):
        self._metadata.genres.clear()

        self._generateEbook()

        self.assertIsNone(self._outputEpub.getSubject())

    def test_default_publisher_in_metadata(self):
        self._generateEbook()

        self.assertEqual(self._outputEpub.getPublisher(), "ePubLibre")

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