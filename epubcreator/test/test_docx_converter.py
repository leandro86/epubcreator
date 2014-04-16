import os
import unittest
import sys

from epubcreator.converters.docx import docx_converter
from epubcreator.test import utils

TESTS_WITH_CUSTOM_OPTIONS = {"character_styles": dict(ignoreEmptyParagraphs=False),
                             "empty_paragraphs_conversion": dict(ignoreEmptyParagraphs=False),
                             "paragraph_styles": dict(ignoreEmptyParagraphs=False),
                             "paragraph_styles_inside_div": dict(ignoreEmptyParagraphs=False)}
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "test_data", "converters", "docx")


class DocxConverterTest(unittest.TestCase):
    pass


def makeTest(docxFilePath, outputFolder, **options):
    def test(self):
        converter = docx_converter.DocxConverter(docxFilePath, **options)
        ebookData = converter.convert()

        for section in ebookData.sections:
            with open(os.path.join(outputFolder, section.name), encoding="utf-8") as file:
                utils.assertXhtmlsAreEqual(section.toHtml(), file.read())

    return test


def generateTests():
    tests = (os.path.join(TEST_DATA_DIR, f) for f in os.listdir(TEST_DATA_DIR) if f.endswith(".docx"))

    for test in tests:
        testName = os.path.split(os.path.splitext(test)[0])[1]
        testExpectedOutputDir = os.path.join(TEST_DATA_DIR, "{0}_output".format(testName))
        options = {}

        if testName in TESTS_WITH_CUSTOM_OPTIONS:
            options = TESTS_WITH_CUSTOM_OPTIONS[testName]

        setattr(DocxConverterTest, "test_{0}".format(testName), makeTest(test, testExpectedOutputDir, **options))


def load_tests(loader, tests, pattern):
    generateTests()
    tests.addTest(loader.loadTestsFromTestCase(DocxConverterTest))
    return tests


if __name__ == '__main__':
    # Si quiero ejecutar algún test en particular, debo pasarlo como argumento de
    # esta forma: DocxConverterTest.test_one_paragraph.
    # En caso de pasar un test como argumento, unittest.main() no llama a load_tests(), que
    # básicamente se encarga de cargar los tests, por lo que debo hacerlo acá explícitamente.
    if len(sys.argv) > 1:
        generateTests()

    unittest.main()