import os
import unittest

from pyepub.pyepubreader import epub


class EpubReaderTests(unittest.TestCase):
    def setUp(self):
        self._epub = epub.EpubReader(os.path.join(os.path.dirname(__file__), "data", "epub_test.epub"))

    def tearDown(self):
        if self._epub:
            self._epub.close()

    def test_html_files_play_order(self):
        htmlFileNames = self._epub.getHtmlFileNamesReadingOrder()
        self.assertEqual(htmlFileNames, ["cubierta.xhtml", "sinopsis.xhtml", "titulo.xhtml", "info.xhtml", "dedicatoria.xhtml",
                                         "Section0001.xhtml", "autor.xhtml", "notas.xhtml"])

    def test_container_content_read(self):
        self.assertIsNotNone(self._epub.read("META-INF/container.xml"))

    def test_read_authors(self):
        authors = self._epub.getAuthors()

        self.assertEqual(len(authors), 2)
        self.assertEqual(authors[0], ("Jorge Luis Borges", "Borges, Jorge Luis"))
        self.assertEqual(authors[1], ("Edgar Allan Poe", "Poe, Edgar Allan"))

    def test_read_translators(self):
        translators = self._epub.getTranslators()

        self.assertEqual(len(translators), 2)
        self.assertEqual(translators[0], ("Pepe Pérez", "Pérez, Pepe"))
        self.assertEqual(translators[1], ("Sancho Panza", "Panza, Sancho"))

    def test_read_ilustrators(self):
        ilustrators = self._epub.getIlustrators()

        self.assertEqual(len(ilustrators), 2)
        self.assertEqual(ilustrators[0], ("Roberto García", "García, Roberto"))
        self.assertEqual(ilustrators[1], ("Marcos Nuñez", "Nuñez, Marcos"))

    def test_read_calibre_series(self):
        calibreSerie = self._epub.getCalibreSerie()

        self.assertEqual(calibreSerie, ("Nombre de la saga", "9"))

    def test_has_file(self):
        self.assertTrue(self._epub.hasFile("cubierta.xhtml"))
        self.assertTrue(self._epub.hasFile("dedicatoria.xhtml"))
        self.assertFalse(self._epub.hasFile("no_existe.xhtml"))

    def test_get_titles(self):
        self.assertEqual(self._epub.getTitles(), [("Cubierta", "Text/cubierta.xhtml"),
                                                  ("Título", "Text/titulo.xhtml"),
                                                  ("Capítulo 1", "Text/Section0001.xhtml"),
                                                  ("Autor", "Text/autor.xhtml"),
                                                  ("Notas", "Text/notas.xhtml")])

    def test_get_full_path_to_file(self):
        self.assertEqual(self._epub.getFullPathToFile("cubierta.xhtml"), "OEBPS/Text/cubierta.xhtml")
        self.assertEqual(self._epub.getFullPathToFile("style.css"), "OEBPS/Styles/style.css")

    def test_description(self):
        self.assertEqual(self._epub.getDescription(), "Sinopsis")

    def test_title(self):
        self.assertEqual(self._epub.getTitle(), "Título")

    def test_language(self):
        self.assertEqual(self._epub.getLanguage(), "es")

    def test_modification_date(self):
        self.assertEqual(self._epub.getModificationDate(), "2013-07-23")

    def test_publication_date(self):
        self.assertEqual(self._epub.getPublicationDate(), "2013-04-23")

    def test_publisher(self):
        self.assertEqual(self._epub.getPublisher(), "ePubLibre")

    def test_subject(self):
        self.assertEqual(self._epub.getSubject(), "Género, Subgéneros")


if __name__ == '__main__':
    unittest.main()
