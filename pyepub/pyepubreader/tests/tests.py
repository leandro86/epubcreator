import os
import unittest

from pyepub.pyepubreader import epub


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self._epub = None


    def tearDown(self):
        if self._epub:
            self._epub.close()


    def testHtmlFilesPlayOrder(self):
        self._epub = epub.EpubReader(os.path.join("data", "epub_test.epub"))

        htmlFileNames = self._epub.getHtmlFileNamesReadingOrder()
        self.assertEqual(htmlFileNames, ["cubierta.xhtml", "sinopsis.xhtml", "titulo.xhtml", "info.xhtml",
                                         "dedicatoria.xhtml", "Section0001.xhtml", "autor.xhtml", "notas.xhtml"])


    def testContainerContentRead(self):
        self._epub = epub.EpubReader(os.path.join("data", "epub_test.epub"))
        self.assertIsNotNone(self._epub.read("META-INF/container.xml"))


    def testReadInvalidFileName(self):
        self._epub = epub.EpubReader(os.path.join("data", "epub_test.epub"))
        self.assertRaises(KeyError, lambda: self._epub.read("bla.xml"))


    def testReadAuthors(self):
        self._epub = epub.EpubReader(os.path.join("data", "epub_test.epub"))
        authors = self._epub.getAuthors()

        self.assertEqual(len(authors), 2)
        self.assertEqual(authors[0], ("Jorge Luis Borges", "Borges, Jorge Luis"))
        self.assertEqual(authors[1], ("Edgar Allan Poe", "Poe, Edgar Allan"))


    def testReadTranslators(self):
        self._epub = epub.EpubReader(os.path.join("data", "epub_test.epub"))
        translators = self._epub.getTranslators()

        self.assertEqual(len(translators), 2)
        self.assertEqual(translators[0], ("Pepe Pérez", "Pérez, Pepe"))
        self.assertEqual(translators[1], ("Sancho Panza", "Panza, Sancho"))

    def testReadIlustrators(self):
        self._epub = epub.EpubReader(os.path.join("data", "epub_test.epub"))
        ilustrators = self._epub.getIlustrators()

        self.assertEqual(len(ilustrators), 2)
        self.assertEqual(ilustrators[0], ("Roberto García", "García, Roberto"))
        self.assertEqual(ilustrators[1], ("Marcos Nuñez", "Nuñez, Marcos"))

    def testReadCalibreSeries(self):
        self._epub = epub.EpubReader(os.path.join("data", "epub_test.epub"))
        calibreSerie = self._epub.getCalibreSerie()

        self.assertEqual(calibreSerie, ("Nombre de la saga", "9"))


if __name__ == '__main__':
    unittest.main()
