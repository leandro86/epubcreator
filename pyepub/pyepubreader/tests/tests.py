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
import unittest

from pyepubreader import epub


class MyTestCase(unittest.TestCase):


    def setUp(self):
        self._epub = None


    def tearDown(self):
        if self._epub:
            self._epub.close()


    def testHtmlFilesPlayOrder(self):
        self._epub = epub.Epub(os.path.join("data", "epub_test.epub"))

        htmlFileNames = self._epub.getHtmlFileNamesReadingOrder()
        self.assertEqual(htmlFileNames, ["cubierta.xhtml", "sinopsis.xhtml", "titulo.xhtml", "info.xhtml",
                                         "dedicatoria.xhtml", "Section0001.xhtml", "autor.xhtml", "notas.xhtml"])


    def testContainerContentRead(self):
        self._epub = epub.Epub(os.path.join("data", "epub_test.epub"))
        self.assertIsNotNone(self._epub.read("META-INF/container.xml"))


    def testReadInvalidFileName(self):
        self._epub = epub.Epub(os.path.join("data", "epub_test.epub"))
        self.assertRaises(KeyError, lambda: self._epub.read("bla.xml"))


    def testReadAuthors(self):
        self._epub = epub.Epub(os.path.join("data", "epub_test.epub"))
        authors = self._epub.getAuthors()

        self.assertEqual(len(authors), 2)
        self.assertEqual(authors[0], ("Jorge Luis Borges", "Borges, Jorge Luis"))
        self.assertEqual(authors[1], ("Edgar Allan Poe", "Poe, Edgar Allan"))


    def testReadTranslators(self):
        self._epub = epub.Epub(os.path.join("data", "epub_test.epub"))
        translators = self._epub.getTranslators()

        self.assertEqual(len(translators), 2)
        self.assertEqual(translators[0], ("Pepe Pérez", "Pérez, Pepe"))
        self.assertEqual(translators[1], ("Sancho Panza", "Panza, Sancho"))

    def testReadIlustrators(self):
        self._epub = epub.Epub(os.path.join("data", "epub_test.epub"))
        ilustrators = self._epub.getIlustrators()

        self.assertEqual(len(ilustrators), 2)
        self.assertEqual(ilustrators[0], ("Roberto García", "García, Roberto"))
        self.assertEqual(ilustrators[1], ("Marcos Nuñez", "Nuñez, Marcos"))

    def testReadCalibreSeries(self):
        self._epub = epub.Epub(os.path.join("data", "epub_test.epub"))
        calibreSerie = self._epub.getCalibreSerie()

        self.assertEqual(calibreSerie, ("Nombre de la saga", "9"))


if __name__ == '__main__':
    unittest.main()
