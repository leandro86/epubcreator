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

import unittest
import tempfile
import datetime

from lxml import etree
from pyepub.pyepubreader import epub

from ecreator import ebook, ebook_data


class TestEbook(unittest.TestCase):

    _NAMESPACES = {"x" : "http://www.w3.org/1999/xhtml"}

    def setUp(self):
        self._outputFile = tempfile.TemporaryFile()
        self._metadata = ebook_data.Metadata()
        self._outputEpub = None

    def tearDown(self):
        self._outputFile.close()
        
        if  self._outputEpub:
            self._outputEpub.close()

    def testCoverFileExists(self):
        self._generateEbook()
        self._getCoverFile()

        try:
            self._outputEpub.read("OEBPS/Images/{0}".format(ebook.Ebook.COVER_IMAGE_EP_NAME))
        except KeyError as e:
            self.fail(e)

    def testTitleFileData(self):
        self._metadata.authors.append(ebook_data.Person("el autor", "el autor"))
        self._metadata.title = "el título"
        self._metadata.subtitle = "el subtítulo"
        self._metadata.editor = "el editor"

        self._generateEbook()
        title = self._getTitleFile()

        self.assertEqual(self._xpath(title, "/x:html/x:body/x:p[@class = 'tautor']/x:code/text()"),
                         ["el autor"])
        self.assertEqual(self._xpath(title, "/x:html/x:body/x:h1[@class = 'ttitulo']/x:strong/text()"),
                         ["el título"])
        self.assertEqual(self._xpath(title, "/x:html/x:body/x:p[@class = 'tsubtitulo']/x:strong/text()"),
                         ["el subtítulo"])
        self.assertEqual(self._xpath(title, "/x:html/x:body/x:p[@class = 'tfirma']/x:strong/text()"),
                         ["el editor"])

        # Debe existir un espacio entre el nombre del editor y la fecha de creación del epub
        self.assertEqual(self._xpath(title, "/x:html/x:body/x:p[@class = 'tfirma']/text()"), [" "])

        self.assertEqual(self._xpath(title, "/x:html/x:body/x:p[@class = 'tfirma']/x:code/text()"),
                         [datetime.datetime.now().strftime("%d.%m.%y")])

    def testInfoFileData(self):
        self._metadata.originalTitle = "el título original"
        self._metadata.authors.append(ebook_data.Person("el autor", "el autor"))
        self._metadata.publicationDate = datetime.date(1756, 1, 1)
        self._metadata.translators.append(ebook_data.Person("el traductor", "el traductor"))
        self._metadata.ilustrators.append(ebook_data.Person("el ilustrador", "el ilustrador"))
        self._metadata.coverDesignOrTweak = "Diseño"
        self._metadata.coverDesigner = "el diseñador de portada"
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
                         ["Diseño de portada: el diseñador de portada"])
        self.assertEqual(self._xpath(info, "/x:html/x:body/x:div[@class = 'info']/x:p[@class = 'salto10']/text()"),
                         ["Editor digital: el editor"])

    def testSynopsisFileData(self):
        self._metadata.synopsis = "Párrafo 1 de la sinopsis.\nPárrafo 2 de la sinopsis.\nPárrafo 3 de la sinopsis."

        self._generateEbook()
        synopsis = self._getSynopsisFile()

        self.assertEqual(self._xpath(synopsis, "/x:html/x:body/x:div[@class = 'sinopsis']/x:p[1]/text()"),
                         ["Párrafo 1 de la sinopsis."])
        self.assertEqual(self._xpath(synopsis, "/x:html/x:body/x:div[@class = 'sinopsis']/x:p[2]/text()"),
                         ["Párrafo 2 de la sinopsis."])
        self.assertEqual(self._xpath(synopsis, "/x:html/x:body/x:div[@class = 'sinopsis']/x:p[3]/text()"),
                         ["Párrafo 3 de la sinopsis."])

    def testDedicationFileData(self):
        self._metadata.dedication = ("Párrafo 1 de la dedicatoria.\nPárrafo 2 de la dedicatoria.\nPárrafo 3 de " \
                                    "la dedicatoria.")

        self._generateEbook()
        dedication = self._getDedicationFile()

        self.assertEqual(self._xpath(dedication, "/x:html/x:body/x:div[@class = 'dedicatoria']/x:p[1]/text()"),
                         ["Párrafo 1 de la dedicatoria."])
        self.assertEqual(self._xpath(dedication, "/x:html/x:body/x:div[@class = 'dedicatoria']/x:p[2]/text()"),
                         ["Párrafo 2 de la dedicatoria."])
        self.assertEqual(self._xpath(dedication, "/x:html/x:body/x:div[@class = 'dedicatoria']/x:p[3]/text()"),
                         ["Párrafo 3 de la dedicatoria."])

    def testNotSubtitleOnTitleData(self):
        self._generateEbook()
        title = self._getTitleFile()

        self.assertFalse(self._xpath(title, "/x:html/x:body/x:p[@class = 'tsubtitulo']"))

        # En titulo.xhtml hay un comentario indicando en el campo de subtítulo que es opcional, por eso debo verificar
        # que también ese comentario se haya borrado
        self.assertFalse(self._xpath(title, "/x:html/x:body/comment()"))

    def testMissingFieldsOnInfoData(self):
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

    def testSynopsisFileExistsIfNotSynopsisText(self):
        self._generateEbook()
        synopsis = self._getSynopsisFile()

        # Si no agrego un texto de sinopsis, entonces por ahora agrego igualmente sinopsis.xhtml al epub, con el texto
        # que viene por defecto en el base.
        self.assertTrue(self._xpath(synopsis,
                                    "/x:html/x:body/x:div[@class = 'sinopsis']/x:p[1]/text()")[0]
                                    .startswith("Yo por bien tengo que cosas tan señaladas"))

    def testDedicationFileExistsIfNotDedicationText(self):
        self._generateEbook()
        dedication = self._getDedicationFile()

        # Al igual que en la sinopsis, si no agregué texto de dedicatoria, igualmente agrego dedicatoria.xhtml
        self.assertTrue(self._xpath(dedication, "/x:html/x:body/x:div[@class = 'dedicatoria']/x:p[1]/text()")[0]
                                                .startswith("Suspiró entonces mío Cid"))

    def testAuthorFileData(self):
        self._metadata.authorBiography = ("Párrafo 1 de la biografía.\nPárrafo 2 de la biografía.\nPárrafo 3 de "
                                          "la biografía.")

        self._generateEbook()
        author = self._getAuthorFile()

        self.assertEqual(self._xpath(author, "/x:html/x:body/x:p[@class = 'asangre' and position() = 2]/text()"),
                         ["Párrafo 1 de la biografía."])
        self.assertEqual(self._xpath(author, "/x:html/x:body/x:p[not(@class) and position() = 3]/text()"),
                         ["Párrafo 2 de la biografía."])
        self.assertEqual(self._xpath(author, "/x:html/x:body/x:p[not(@class) and position() = 4]/text()"),
                         ["Párrafo 3 de la biografía."])

        # Compruebo que exista la imagen del autor, ya que autor.xhtml la referencia
        try:
            self._outputEpub.read("OEBPS/Images/{0}".format(ebook.Ebook.AUTHOR_IMAGE_EP_NAME))
        except KeyError as e:
            self.fail(e)

        # Compruebo que el archivo del autor sea el último (ya que así lo indica el epubbase. En realidad indica que
        # debe ser el último antes de notas.xhtml, pero acá no agrego notas, me basta con chequear por el último.)
        htmlFiles = self._outputEpub.getHtmlFileNamesReadingOrder()
        self.assertEqual(htmlFiles[-1], ebook.Ebook.AUTHOR_EP_NAME)

    def testAuthorFileExistsIfNotAuthorBiography(self):
        self._generateEbook()
        author = self._getAuthorFile()

        # Compruebo que autor.xhtml se haya agregado cuando no especifiqué una biografía de autor.
        self.assertTrue(self._xpath(author, "/x:html/x:body/x:p[@class = 'asangre' and position() = 2]/text()")[0]
                                            .startswith("NOMBRE DEL AUTOR. Lorem ipsum dolor"))

    def testAuthorFileIsSecondToLastWhenEbookContainsNotes(self):
        files = [ebook_data.File(ebook.Ebook.NOTES_EP_NAME, ebook_data.File.FILE_TYPE.TEXT, "bla")]
        self._generateEbook(files)

        htmlFiles = self._outputEpub.getHtmlFileNamesReadingOrder()
        self.assertEqual(htmlFiles[-2], ebook.Ebook.AUTHOR_EP_NAME)

    def testMultipleAuthors(self):
        self._metadata.authors.append(ebook_data.Person("Jorge Luis Borges", "Borges, Jorge Luis"))
        self._metadata.authors.append(ebook_data.Person("Edgar Allan Poe", "Poe, Edgar Allan"))
        self._metadata.authors.append(ebook_data.Person("William Shakespeare", "Shakespeare, William"))
        self._metadata.authors.append(ebook_data.Person("G. K. Chesterton", "Chesterton, G. K."))

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

    def testMultipleTranslators(self):
        self._metadata.translators.append(ebook_data.Person("Jorge Luis Borges", "Borges, Jorge Luis"))
        self._metadata.translators.append(ebook_data.Person("Edgar Allan Poe", "Poe, Edgar Allan"))
        self._metadata.translators.append(ebook_data.Person("William Shakespeare", "Shakespeare, William"))
        self._metadata.translators.append(ebook_data.Person("G. K. Chesterton", "Chesterton, G. K."))

        self._generateEbook()
        info = self._getInfoFile()

        self.assertEqual(self._xpath(info, "/x:html/x:body/x:div[@class = 'info']/x:p[2]/text()"),
                         ["Traducción: Jorge Luis Borges & Edgar Allan Poe & William Shakespeare & G. K. Chesterton"])

        # Compruebo que en los metadatos se hayan agregado los traductores correctamente
        translators = self._outputEpub.getTranslators()
        self.assertEqual(len(translators), 4)
        self.assertEqual(translators[0], ("Jorge Luis Borges", "Borges, Jorge Luis"))
        self.assertEqual(translators[1], ("Edgar Allan Poe", "Poe, Edgar Allan"))
        self.assertEqual(translators[2], ("William Shakespeare", "Shakespeare, William"))
        self.assertEqual(translators[3], ("G. K. Chesterton", "Chesterton, G. K."))

    def testMultipleIlustrators(self):
        self._metadata.ilustrators.append(ebook_data.Person("Jorge Luis Borges", "Borges, Jorge Luis"))
        self._metadata.ilustrators.append(ebook_data.Person("Edgar Allan Poe", "Poe, Edgar Allan"))
        self._metadata.ilustrators.append(ebook_data.Person("William Shakespeare", "Shakespeare, William"))
        self._metadata.ilustrators.append(ebook_data.Person("G. K. Chesterton", "Chesterton, G. K."))

        self._generateEbook()
        info = self._getInfoFile()

        self.assertEqual(self._xpath(info, "/x:html/x:body/x:div[@class = 'info']/x:p[2]/text()"),
                         ["Ilustraciones: Jorge Luis Borges & Edgar Allan Poe & William Shakespeare & G. K. "
                          "Chesterton"])

        # Compruebo que en los metadatos se hayan agregado los ilustradores correctamente
        ilustrators = self._outputEpub.getIlustrators()
        self.assertEqual(len(ilustrators), 4)
        self.assertEqual(ilustrators[0], ("Jorge Luis Borges", "Borges, Jorge Luis"))
        self.assertEqual(ilustrators[1], ("Edgar Allan Poe", "Poe, Edgar Allan"))
        self.assertEqual(ilustrators[2], ("William Shakespeare", "Shakespeare, William"))
        self.assertEqual(ilustrators[3], ("G. K. Chesterton", "Chesterton, G. K."))

    def testSimpleCollection(self):
        self._metadata.subCollectionName = "Esta es la saga"
        self._metadata.collectionVolume = "9"

        self._generateEbook()

        calibreSerie = self._outputEpub.getCalibreSerie()
        self.assertEqual(calibreSerie, ("Esta es la saga", "9"))

    def testSubCollections(self):
        self._metadata.collectionName = "Esta es la serie"
        self._metadata.subCollectionName = "Esta es la saga"
        self._metadata.collectionVolume = "9"

        self._generateEbook()

        calibreSerie = self._outputEpub.getCalibreSerie()
        self.assertEqual(calibreSerie, ("Esta es la serie: Esta es la saga", "9"))

    def testStripZerosFromCollectionVolumeForCalibreMetadata(self):
        self._metadata.subCollectionName = "Esta es la saga"
        self._metadata.collectionVolume = "007"

        self._generateEbook()

        calibreSerie = self._outputEpub.getCalibreSerie()
        self.assertEqual(calibreSerie, ("Esta es la saga", "7"))

    def testEpubFileNameOneAuthorNoCollection(self):
        self._metadata.title = "Título del libro"
        self._metadata.editor = "Editor del libro"
        self._metadata.authors.append(ebook_data.Person("Juan Pérez", "Pérez, Juan"))

        fileName = self._generateEbook()

        self.assertEqual(fileName, "Perez, Juan - Titulo del libro (r1.0 Editor del libro).epub")

    def testEpubFileNameTwoAuthorsNoCollection(self):
        self._metadata.title = "Título del libro"
        self._metadata.editor = "Editor del libro"
        self._metadata.authors.append(ebook_data.Person("Juan Pérez", "Pérez, Juan"))
        self._metadata.authors.append(ebook_data.Person("Roberto Gómez", "Gómez, Roberto"))

        fileName = self._generateEbook()

        self.assertEqual(fileName, "Perez, Juan & Gomez, Roberto - Titulo del libro (r1.0 Editor del libro).epub")

    def testEpubFileNameThreeAuthorsNoCollection(self):
        self._metadata.title = "Título del libro"
        self._metadata.editor = "Editor del libro"
        self._metadata.authors.append(ebook_data.Person("Juan Pérez", "Pérez, Juan"))
        self._metadata.authors.append(ebook_data.Person("Roberto Gómez", "Gómez, Roberto"))
        self._metadata.authors.append(ebook_data.Person("Sancho Panza", "Panza, Sancho"))

        fileName = self._generateEbook()

        self.assertEqual(fileName, "AA. VV. - Titulo del libro (r1.0 Editor del libro).epub")

    def testEpubFileNameOneAuthorSimpleCollection(self):
        self._metadata.title = "Título del libro"
        self._metadata.editor = "Editor del libro"
        self._metadata.authors.append(ebook_data.Person("Juan Pérez", "Pérez, Juan"))
        self._metadata.subCollectionName = "Esta es la serie"
        self._metadata.collectionVolume = "10"

        fileName = self._generateEbook()

        self.assertEqual(fileName, "Perez, Juan - [Esta es la serie 10] Titulo del libro (r1.0 Editor del libro).epub")

    def testEpubFileNameOneAuthorSubCollection(self):
        self._metadata.title = "Título del libro"
        self._metadata.editor = "Editor del libro"
        self._metadata.authors.append(ebook_data.Person("Juan Pérez", "Pérez, Juan"))
        self._metadata.collectionName = "Esta es la saga"
        self._metadata.subCollectionName = "Esta es la serie"
        self._metadata.collectionVolume = "10"

        fileName = self._generateEbook()

        self.assertEqual(fileName, "[Esta es la saga] [Esta es la serie 10] Perez, Juan - Titulo del libro (r1.0 Editor del libro).epub")

    def testEpubFileNameTwoAuthorsubCollection(self):
        self._metadata.title = "Título del libro"
        self._metadata.editor = "Editor del libro"
        self._metadata.authors.append(ebook_data.Person("Juan Pérez", "Pérez, Juan"))
        self._metadata.authors.append(ebook_data.Person("Roberto Gómez", "Gómez, Roberto"))
        self._metadata.collectionName = "Esta es la saga"
        self._metadata.subCollectionName = "Esta es la serie"
        self._metadata.collectionVolume = "10"

        fileName = self._generateEbook()

        self.assertEqual(fileName,
                         "[Esta es la saga] [Esta es la serie 10] Perez, Juan & Gomez, Roberto - Titulo del libro (r1.0 Editor del libro).epub")

    def _generateEbook(self, files = None):
        eebook = ebook.Ebook(files=files, metadata=self._metadata)
        fileName = eebook.save(self._outputFile)
        self._outputEpub = epub.EpubReader(self._outputFile)
        return fileName

    def _getInfoFile(self):
        try:
            return etree.XML(self._outputEpub.read("OEBPS/Text/{0}".format(ebook.Ebook.INFO_EP_NAME)))
        except KeyError as e:
            self.fail(e)

    def _getTitleFile(self):
        try:
            return etree.XML(self._outputEpub.read("OEBPS/Text/{0}".format(ebook.Ebook.TITLE_EP_NAME)))
        except KeyError as e:
            self.fail(e)

    def _getSynopsisFile(self):
        try:
            synopsis = self._outputEpub.read("OEBPS/Text/{0}".format(ebook.Ebook.SYNOPSIS_EP_NAME))

            # Tengo que eliminar la entidad nbsp de la sinopsis, ya que sino lxml se queja y no pueda parsear el xml
            purgedSynopsis = synopsis.decode("utf-8").replace("<p>&nbsp;</p>", "")

            return etree.XML(bytes(purgedSynopsis, "utf-8"))
        except KeyError as e:
            self.fail(e)

    def _getDedicationFile(self):
        try:
            return etree.XML(self._outputEpub.read("OEBPS/Text/{0}".format(ebook.Ebook.DEDICATION_EP_NAME)))
        except KeyError as e:
            self.fail(e)

    def _getAuthorFile(self):
        try:
            return etree.XML(self._outputEpub.read("OEBPS/Text/{0}".format(ebook.Ebook.AUTHOR_EP_NAME)))
        except KeyError as e:
            self.fail(e)

    def _getCoverFile(self):
        try:
            return etree.XML(self._outputEpub.read("OEBPS/Text/{0}".format(ebook.Ebook.COVER_EP_NAME)))
        except KeyError as e:
            self.fail(e)

    def _xpath(self, element, xpath):
        """
        Ejecuta una expresión xpath en un elemento.

        @param element: el elemento en el cual ejecuctar la expresión.
        @param xpath: la expresión xpath a ejecutar.

        @return: el resultado de la expresión xpath.
        """
        return element.xpath(xpath, namespaces = TestEbook._NAMESPACES)


if __name__ == "__main__":
    unittest.main()