import os
import unittest
import re

from lxml import etree

from epubcreator.converters.docx import docx_converter


class DocxConverterTests(unittest.TestCase):
    def setUp(self):
        self._pathToTestDataFolder = os.path.join(os.path.dirname(__file__), "test_data")

    def test_one_paragraph(self):
        data = self._getOutput("one_paragraph.docx")

        self.assertEqual(len(data.sections), 1)
        self.assertTrue(self._compareSections("one_paragraph.docx", data.sections))

    def test_pagebreaks_with_br(self):
        data = self._getOutput("pagebreaks_with_br.docx")

        self.assertEqual(len(data.sections), 5)
        self.assertTrue(self._compareSections("pagebreaks_with_br.docx", data.sections))

    def test_pagebreaks_with_pagebreakbefore(self):
        data = self._getOutput("pagebreaks_with_pagebreakbefore.docx")

        self.assertEqual(len(data.sections), 4)
        self.assertTrue(self._compareSections("pagebreaks_with_pagebreakbefore.docx", data.sections))

    def test_english_headings(self):
        # Testeo los títulos cuando el nombre de los estilos de los mismos tienen nombre en
        # inglés: "heading 1", "heading 2", etc.
        data = self._getOutput("english_headings.docx")

        self.assertEqual(len(data.sections), 1)
        self.assertTrue(self._compareSections("english_headings.docx", data.sections))

        self.assertEqual(data.toc.getFirstLevelTitlesCount(), 1)
        self.assertEqual(data.toc.getTotalTitlesCount(), 6)

        h1 = data.toc.titles[0]
        self.assertEqual(h1.text, "Capítulo 1")
        self.assertEqual(h1.titleLocation, "Section0000.xhtml#heading_id_1")

        h2 = h1.childTitles[0]
        self.assertEqual(h2.text, "Capítulo 2")
        self.assertEqual(h2.titleLocation, "Section0000.xhtml#heading_id_2")

        h3 = h2.childTitles[0]
        self.assertEqual(h3.text, "Capítulo 3")
        self.assertEqual(h3.titleLocation, "Section0000.xhtml#heading_id_3")

        h4 = h3.childTitles[0]
        self.assertEqual(h4.text, "Capítulo 4")
        self.assertEqual(h4.titleLocation, "Section0000.xhtml#heading_id_4")

        h5 = h4.childTitles[0]
        self.assertEqual(h5.text, "Capítulo 5")
        self.assertEqual(h5.titleLocation, "Section0000.xhtml#heading_id_5")

        h6 = h5.childTitles[0]
        self.assertEqual(h6.text, "Capítulo 6")
        self.assertEqual(h6.titleLocation, "Section0000.xhtml#heading_id_6")

    def test_spanish_headings(self):
        # Testeo los títulos cuando el nombre de los estilos de los mismos tienen nombre en
        # español: "encabezado 1", "encabezado 2", etc.
        data = self._getOutput("spanish_headings.docx")

        self.assertEqual(len(data.sections), 1)
        self.assertTrue(self._compareSections("spanish_headings.docx", data.sections))

        self.assertEqual(data.toc.getFirstLevelTitlesCount(), 1)
        self.assertEqual(data.toc.getTotalTitlesCount(), 6)

    def test_formats(self):
        data = self._getOutput("formats.docx")

        self.assertEqual(len(data.sections), 1)
        self.assertTrue(self._compareSections("formats.docx", data.sections))

    def test_headings_nested(self):
        data = self._getOutput("headings_nested.docx")

        self.assertEqual(len(data.sections), 22)
        self.assertTrue(self._compareSections("headings_nested.ocx", data.sections))

        self.assertEqual(data.toc.getFirstLevelTitlesCount(), 3)
        self.assertEqual(data.toc.getTotalTitlesCount(), 22)

    def test_headings_with_format(self):
        data = self._getOutput("headings_with_format.docx")

        self.assertEqual(len(data.sections), 4)
        self.assertTrue(self._compareSections("headings_with_format.docx", data.sections))

        self.assertEqual(data.toc.getTotalTitlesCount(), 4)
        self.assertEqual(data.toc.titles[0].text, "Capítulo 1 subrayado.")
        self.assertEqual(data.toc.titles[1].text, "Capítulo 2 en itálica.")
        self.assertEqual(data.toc.titles[2].text, "Capítulo 3 subrayado y en itálica.")
        self.assertEqual(data.toc.titles[3].text, "Capítulo 4 que combina diferentes estilos. Esta parte está en itálica, y esta otra "
                                                  "subrayada. Esta parte está en itálica y subrayada.")

    def test_heading_with_footnote(self):
        data = self._getOutput("heading_with_footnote.docx")

        self.assertEqual(len(data.sections), 2)
        self.assertTrue(self._compareSections("heading_with_footnote.docx", data.sections))

        self.assertEqual(data.toc.getTotalTitlesCount(), 1)
        self.assertEqual(data.toc.titles[0].text, "Título 1 que contiene una nota al pie.")

    def test_paragraph_styles(self):
        # Testea estilos que se aplican a todoo el párrafo, lo que en word se
        # denomina "estilos vinculados a párrafo".
        data = self._getOutput("paragraph_styles.docx", False)

        self.assertEqual(len(data.sections), 1)
        self.assertTrue(self._compareSections("paragraph_styles.docx", data.sections))

    def test_character_styles(self):
        # Testea estilos que son aplicados a nivel carácter, es decir, que pueden
        # aplicarse a partes dentro del párrafo. Para ello necesito utilizar la
        # etiqueta span.
        data = self._getOutput("character_styles.docx", False)

        self.assertEqual(len(data.sections), 1)
        self.assertTrue(self._compareSections("character_styles.docx", data.sections))

    def test_paragraph_styles_inside_div(self):
        # Si dos o más párrafos consecutivos comparten el mismo estilo vinculado a
        # párrafo, entonces deben ir dentro de un div.
        data = self._getOutput("paragraph_styles_inside_div.docx", False)

        self.assertEqual(len(data.sections), 3)
        self.assertTrue(self._compareSections("paragraph_styles_inside_div.docx", data.sections))

    def test_footnotes(self):
        data = self._getOutput("footnotes.docx")

        self.assertEqual(len(data.sections), 3)
        self.assertTrue(self._compareSections("footnotes.docx", data.sections))

    def test_multiple_paragraphs_in_footnotes(self):
        data = self._getOutput("multiple_paragraphs_in_footnotes.docx")

        self.assertEqual(len(data.sections), 2)
        self.assertTrue(self._compareSections("multiple_paragraphs_in_footnotes.docx", data.sections))

    def test_empty_paragraphs_conversion(self):
        data = self._getOutput("empty_paragraphs_conversion.docx", False)

        self.assertEqual(len(data.sections), 3)
        self.assertTrue(self._compareSections("empty_paragraphs_conversion.docx", data.sections))

    def test_empty_paragraphs_ignore(self):
        data = self._getOutput("empty_paragraphs_ignore.docx")

        self.assertEqual(len(data.sections), 1)
        self.assertTrue(self._compareSections("empty_paragraphs_ignore.docx", data.sections))

    def test_images(self):
        data = self._getOutput("images.docx")

        self.assertEqual(len(data.sections), 1)
        self.assertEqual(len(data.images), 9)

        self.assertTrue(self._compareSections("images.docx", data.sections))

    def test_broken_headings(self):
        data = self._getOutput("broken_headings.docx")

        self.assertEqual(len(data.sections), 1)
        self.assertTrue(self._compareSections("broken_headings.docx", data.sections))

    def test_shape(self):
        data = self._getOutput("shape.docx")

        self.assertEqual(len(data.sections), 1)
        self.assertTrue(self._compareSections("shape.docx", data.sections))

    def test_styles_with_formats(self):
        data = self._getOutput("styles_with_formats.docx")

        self.assertEqual(len(data.sections), 1)
        self.assertTrue(self._compareSections("styles_with_formats.docx", data.sections))

    def test_unordered_list(self):
        data = self._getOutput("unordered_list.docx")

        self.assertEqual(len(data.sections), 1)
        self.assertTrue(self._compareSections("unordered_list.docx", data.sections))

    def test_table(self):
        data = self._getOutput("table.docx")

        self.assertEqual(len(data.sections), 1)
        self.assertTrue(self._compareSections("table.docx", data.sections))

    def test_hyperlinks(self):
        data = self._getOutput("hyperlinks.docx")

        self.assertEqual(len(data.sections), 1)
        self.assertTrue(self._compareSections("hyperlinks.docx", data.sections))

    def test_footnotes_images(self):
        data = self._getOutput("footnotes_images.docx")

        self.assertEqual(len(data.sections), 2)
        self.assertTrue(self._compareSections("footnotes_images.docx", data.sections))

    def _compareSections(self, docxTestFileName, sections):
        for section in sections:
            expectedOutput = self._readExpectedOutput(docxTestFileName, section.name)
            self.assertTrue(_XmlComparer.compare(section.toHtml(), expectedOutput))
        return True

    def _readExpectedOutput(self, docxTestFileName, fileName):
        testName = os.path.splitext(docxTestFileName)[0]
        with open(os.path.join(self._pathToTestDataFolder, "{0}_output".format(testName), fileName), encoding="utf-8") as file:
            return file.read()

    def _getOutput(self, docxTestFileName, ignoreEmptyParagraphs=True):
        pathToDocxTestFile = os.path.join(self._pathToTestDataFolder, docxTestFileName)
        transformer = docx_converter.DocxConverter(pathToDocxTestFile, ignoreEmptyParagraphs)
        ebookData = transformer.convert()
        return ebookData

    def _saveSectionsToDisk(self, sections, folderPath):
        for section in sections:
            with open(os.path.join(folderPath, section.name), "w", encoding="utf-8") as outputFile:
                outputFile.write(section.toHtml())

    def _printSections(self, sections):
        for section in sections:
            print("****** BEGIN SECTION ******")
            outputXml = etree.fromstring(section.toHtml().encode())
            print(etree.tostring(outputXml, encoding="utf-8", pretty_print=True).decode())
            print("****** END SECTION ******")


class _XmlComparer:
    """
    Clase para comparar dos archivos xml.
    Parte del código sacado de: https://bitbucket.org/ianb/formencode/src/tip/formencode/doctest_xml_compare.py
    """

    @staticmethod
    def compare(x1, x2):
        # Normalizo los xmls de una forma bastante tosca, pero que me permite preservar los espacios
        # en el texto. Otra opción sería serializar el xml mediante lxml, pero resulta que los atributos
        # no mantienen ningún orden específico al hacerlo.
        normalizedX1 = re.sub(r"\n\s*<", "<", x1)
        normalizedX2 = re.sub(r"\n\s*<", "<", x2)

        return _XmlComparer._performCompare(etree.fromstring(bytes(normalizedX1, "utf-8")),
                                            etree.fromstring(bytes(normalizedX2, "utf-8")))

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
        return (t1 or '') == (t2 or '')


if __name__ == '__main__':
    unittest.main()
