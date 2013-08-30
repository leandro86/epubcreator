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

from lxml import etree

from ecreator.transformers import transformer_base, docx_transformer
from ecreator import ebook_data


class DocxTransformerTests(unittest.TestCase):

    def testOneParagraph(self):
        files = self._getOutput("one_paragraph.docx")[0]

        self.assertEqual(len(files), 1)
        self.assertTrue(self._comparefiles("one_paragraph.docx", files))

    def testPageBreaksWithBr(self):
        files = self._getOutput("pagebreaks_with_br.docx")[0]

        self.assertEqual(len(files), 5)
        self.assertTrue(self._comparefiles("pagebreaks_with_br.docx", files))

    def testPageBreaksWithPageBreakBefore(self):
        files = self._getOutput("pagebreaks_with_pagebreakbefore.docx")[0]

        self.assertEqual(len(files), 4)
        self.assertTrue(self._comparefiles("pagebreaks_with_pagebreakbefore.docx", files))

    def testPageBreaksWithMixed(self):
        files = self._getOutput("pagebreaks_with_mixed.docx")[0]

        self.assertEqual(len(files), 6)
        self.assertTrue(self._comparefiles("pagebreaks_with_mixed.docx", files))

    def testEnglishHeadings(self):
        # Testeo los títulos cuando el nombre de los estilos de los mismos tienen nombre en
        # inglés: "heading 1", "heading 2", etc.
        files = self._getOutput("english_headings.docx")[0]

        self.assertEqual(len(files), 1)
        self.assertTrue(self._comparefiles("english_headings.docx", files))

    def testSpanishHeadings(self):
        # Testeo los títulos cuando el nombre de los estilos de los mismos tienen nombre en
        # español: "encabezado 1", "encabezado 2", etc.
        files = self._getOutput("spanish_headings.docx")[0]

        self.assertEqual(len(files), 1)
        self.assertTrue(self._comparefiles("spanish_headings.docx", files))

    def testFormats(self):
        files = self._getOutput("formats.docx")[0]

        self.assertEqual(len(files), 1)
        self.assertTrue(self._comparefiles("formats.docx", files))

    def testHeadingsNested(self):
        files = self._getOutput("headings_nested.docx")[0]

        self.assertEqual(len(files), 22)
        self.assertTrue(self._comparefiles("headings_nested.ocx", files))

    def testHeadingsWithFormat(self):
        files, titles = self._getOutput("headings_with_format.docx")[:2]

        self.assertEqual(len(files), 4)
        self.assertTrue(self._comparefiles("headings_with_format.docx", files))

        self.assertEqual(len(titles), 4)
        self.assertEqual(titles[0].text, "Capítulo 1 subrayado.")
        self.assertEqual(titles[1].text, "Capítulo 2 en itálica.")
        self.assertEqual(titles[2].text, "Capítulo 3 subrayado y en itálica.")
        self.assertEqual(titles[3].text, "Capítulo 4 que combina diferentes estilos. Esta parte está en itálica, y "
                                         "esta otra subrayada. Esta parte está en itálica y subrayada.")

    def testHeadingWithFootnote(self):
        files, titles = self._getOutput("heading_with_footnote.docx")[:2]

        self.assertEqual(len(files), 2)
        self.assertTrue(self._comparefiles("heading_with_footnote.docx", files))

        self.assertEqual(len(titles), 2)
        self.assertEqual(titles[0].text, "Título 1 que contiene una nota al pie.")

    def testCustomStyles(self):
        files = self._getOutput("custom_styles.docx", False)[0]

        self.assertEqual(len(files), 1)
        self.assertTrue(self._comparefiles("custom_styles.docx", files))

    def testFootnotes(self):
        files = self._getOutput("footnotes.docx")[0]

        self.assertEqual(len(files), 3)
        self.assertTrue(self._comparefiles("footnotes.docx", files))

    def testFootnotesLibreoffice(self):
        # En libreoffice (y creo que algún word viejo también) el id de las notas
        # no necesariamente empieza a contar desde 1, sino que puede hacerlo desde
        # cualquier otro número. En este docx que uso como test, los ids empiezan desde
        # 2, pero obviamente en el epub resultante debo asegurarme que SIEMPRE las notas
        # empiecen a numerarse desde 1.

        files = self._getOutput("footnotes_libreoffice.docx")[0]

        self.assertEqual(len(files), 3)
        self.assertTrue(self._comparefiles("footnotes_libreoffice.docx", files))

    def testEmptyParagraphsConversion(self):
        files = self._getOutput("empty_paragraphs_conversion.docx", False)[0]

        self.assertEqual(len(files), 1)
        self.assertTrue(self._comparefiles("empty_paragraphs_conversion.docx", files))

    def testEmptyParagraphsIgnore(self):
        files = self._getOutput("empty_paragraphs_ignore.docx")[0]

        self.assertEqual(len(files), 1)
        self.assertTrue(self._comparefiles("empty_paragraphs_ignore.docx", files))

    def testImages(self):
        files = self._getOutput("images.docx")[0]

        # La sección más las 7 imágenes
        self.assertEqual(len(files), 7)

        self.assertTrue(self._comparefiles("images.docx", files))

    def testBrokenHeadings(self):
        files, titles = self._getOutput("broken_headings.docx")[:2]

        self.assertEqual(len(files), 1)
        self.assertTrue(self._comparefiles("broken_headings.docx", files))

    def testNestedParagraphs(self):
        files, _, logMessages = self._getOutput("nested_paragraphs.docx")

        self.assertEqual(len(files), 1)
        self.assertTrue(self._comparefiles("nested_paragraphs.docx", files))

        self.assertEqual(len(logMessages), 4)

        self.assertTrue(logMessages[0].msgType == transformer_base.TransformerLogMessage.MSG_TYPE.WARNING)
        self.assertTrue("Se encontró un párrafo anidado" in logMessages[0].message)

        self.assertTrue(logMessages[1].msgType == transformer_base.TransformerLogMessage.MSG_TYPE.WARNING)
        self.assertTrue("Se encontró un párrafo anidado" in logMessages[1].message)

        self.assertTrue(logMessages[2].msgType == transformer_base.TransformerLogMessage.MSG_TYPE.WARNING)
        self.assertTrue("Se encontró un párrafo anidado" in logMessages[2].message)

        self.assertTrue(logMessages[3].msgType == transformer_base.TransformerLogMessage.MSG_TYPE.WARNING)
        self.assertTrue("Se encontró un párrafo anidado" in logMessages[3].message)

    def testShape(self):
        files, _, logMessages = self._getOutput("shape.docx")

        self.assertEqual(len(files), 1)
        self.assertTrue(self._comparefiles("shape.docx", files))

        self.assertEqual(len(logMessages), 2)

        self.assertTrue(logMessages[0].msgType == transformer_base.TransformerLogMessage.MSG_TYPE.WARNING)
        self.assertTrue("Se encontró una figura geométrica" in logMessages[0].message)

        self.assertTrue(logMessages[1].msgType == transformer_base.TransformerLogMessage.MSG_TYPE.WARNING)
        self.assertTrue("Se encontró un párrafo anidado" in logMessages[1].message)

    def testInvalidImageFormat(self):
        files, _, logMessages = self._getOutput("invalid_image_format.docx")

        self.assertEqual(len(files), 1)
        self.assertTrue(self._comparefiles("invalid_image_format.docx", files))

        self.assertEqual(len(logMessages), 1)
        self.assertTrue(logMessages[0].msgType == transformer_base.TransformerLogMessage.MSG_TYPE.WARNING)
        self.assertTrue("Se encontró una imagen con un formato no válido" in logMessages[0].message)

    def testStylesWithFormats(self):
        files = self._getOutput("styles_with_formats.docx")[0]

        self.assertEqual(len(files), 1)
        self.assertTrue(self._comparefiles("styles_with_formats.docx", files))

    def _comparefiles(self, testFileName, files):
        """
        Compara los archivos pertenecientes a un test, con la salida correspondiente
        esperada.

        @param testFileName: el nombre del archivo del test.
        @param files: una lista de File con los archivos a comparar.

        @return: True, si la  comparación fue exitosa. Caso contrario se va a disparar
                 una excepción.
        """
        for textFile in [f for f in files if f.fileType == ebook_data.File.FILE_TYPE.TEXT]:
            expectedOutput = self._readExpectedOutput(testFileName, textFile.name)
            self.assertTrue(_XmlComparer.compare(textFile.content, expectedOutput))
        return True

    def _readExpectedOutput(self, testFileName, fileName):
        """
        Dado un nombre de archivo perteneciente a algún test, retorna el contenido esperado
        correspondiente.

        @param testFileName: el nombre del archivo del test.
        @param fileName: el nombre del archivo a leer perteneciente al test.

        @return: un string con el contenido del archivo.
        """
        testName = os.path.splitext(testFileName)[0]
        with open(os.path.join("test_data", "{0}_output".format(testName), fileName),
                  encoding = "utf-8") as file:
            return file.read()

    def _getOutput(self, docxTestFileName, ignoreEmptyParagraphs = True):
        transformer = docx_transformer.DocxTransformer(os.path.join("test_data", docxTestFileName),
                                                       ignoreEmptyParagraphs)
        files, titles, logMessages = transformer.transform()
        return files, titles, logMessages

    def _saveFileToDisk(self, files, folderPath):
        for file in [f for f in files if f.fileType == ebook_data.File.FILE_TYPE.TEXT]:
            with open(os.path.join(folderPath, file.name), "w", encoding = "utf-8") as outputFile:
                outputFile.write(file.content)

    def _printFiles(self, files):
        for file in files:
            print(file.content)


class _XmlComparer:

    """
    Clase para comparar dos xmls.
    Parte del código sacado de: https://bitbucket.org/ianb/formencode/src/tip/formencode/doctest_xml_compare.py
    """

    @staticmethod
    def compare(x1, x2):
        """
        Compara dos xmls. Ambos deben ser válidos.

        @param x1: un string, con el primer xml
        @param x2: un string, con el segundo xml.

        @return: True/False, dependiendo de si los xmls son iguales o no. Además, imprime en consola las
                 diferencias, si las hay.
        """
        return _XmlComparer._performCompare(etree.XML(bytes(x1, "utf-8")), etree.XML(bytes(x2, "utf-8")))

    @staticmethod
    def _performCompare(x1, x2):
        if x1.tag != x2.tag:
            print('Tags do not match: %s and %s' % (x1.tag, x2.tag))
            return False
        for name, value in x1.attrib.items():
            if x2.attrib.get(name) != value:
                print('Attributes do not match: %s=%r, %s=%r' % (name, value, name, x2.attrib.get(name)))
                return False
        for name in x2.attrib.keys():
            if name not in x1.attrib:
                print('x2 has an attribute x1 is missing: %s' % name)
                return False
        if not _XmlComparer._textComparer(x1.text, x2.text):
            print('text: %r != %r' % (x1.text, x2.text))
            return False
        if not _XmlComparer._textComparer(x1.tail, x2.tail):
            print('tail: %r != %r' % (x1.tail, x2.tail))
            return False
        cl1 = x1.getchildren()
        cl2 = x2.getchildren()
        if len(cl1) != len(cl2):
            print('children length differs, %i != %i'
                         % (len(cl1), len(cl2)))
            return False
        i = 0
        for c1, c2 in zip(cl1, cl2):
            i += 1
            if not _XmlComparer._performCompare(c1, c2):
                print('children %i do not match: %s' % (i, c1.tag))
                return False
        return True

    @staticmethod
    def _textComparer(t1, t2):
        if not t1 and not t2:
            return True
        if t1 == '*' or t2 == '*':
            return True
        return (t1 or '').strip() == (t2 or '').strip()


if __name__ == '__main__':
    unittest.main()
