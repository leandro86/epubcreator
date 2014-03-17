import unittest
import zipfile
import tempfile
import subprocess
import os
import datetime

from lxml import etree

import pyepub.pyepubwriter.epub
import pyepub.pyepubwriter.toc
import pyepub.pyepubwriter.opf


class EpubWriterTests(unittest.TestCase):
    _NAMESPACES = {"opf": pyepub.pyepubwriter.opf.Opf.OPF_NS,
                   "dc": pyepub.pyepubwriter.opf.Opf.DC_NS,
                   "toc": pyepub.pyepubwriter.toc.Toc.TOC_NS}

    def setUp(self):
        self._outputFile = tempfile.TemporaryFile()
        self._epub = pyepub.pyepubwriter.epub.EpubWriter()
        self._resultingEpub = None

    def tearDown(self):
        self._outputFile.close()

        if self._resultingEpub:
            self._resultingEpub.close()

    def test_content_of_mimetype_and_container(self):
        containerContent = (b'<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<container version="1.0" '
                            b'xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n  <rootfiles>\n    '
                            b'<rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>\n  '
                            b'</rootfiles>\n</container>\n')
        mimetypeContent = b"application/epub+zip"

        self._generateEpub()

        try:
            self.assertEqual(self._resultingEpub.getinfo("mimetype").compress_type, zipfile.ZIP_STORED)
            self.assertEqual(self._resultingEpub.read("mimetype"), mimetypeContent)

            self.assertEqual(self._resultingEpub.read("META-INF/container.xml"), containerContent)
        except KeyError as e:
            self.fail(e)

    def test_if_htmls_were_added_to_content_folder(self):
        self._epub.addHtmlData("Section0000.xhtml", "bla")
        self._epub.addHtmlData("Section0001.xhtml", "bla")
        self._epub.addHtmlData("Section0002.xhtml", "bla")

        self._generateEpub()

        try:
            self._resultingEpub.getinfo("OEBPS/Text/Section0000.xhtml")
            self._resultingEpub.getinfo("OEBPS/Text/Section0001.xhtml")
            self._resultingEpub.getinfo("OEBPS/Text/Section0002.xhtml")
        except KeyError as e:
            self.fail(e)

    def test_opf_manifest_and_spine_with_htmls(self):
        self._epub.addHtmlData("Section0000.xhtml", "bla")
        self._epub.addHtmlData("Section0001.xhtml", "bla")

        self._generateEpub()

        opf = self._getOpf()

        self.assertEqual(len(self._xpath(opf, "/opf:package[@unique-identifier = 'BookId' and @version = '2.0']")), 1)
        self.assertEqual(len(self._xpath(opf, "/opf:package/opf:manifest/opf:item[@href = 'toc.ncx' and "
                                              "@id = 'ncx' and @media-type = 'application/x-dtbncx+xml']")), 1)
        self.assertEqual(len(self._xpath(opf, "/opf:package/opf:manifest/opf:item[@href = 'Text/Section0000.xhtml' and "
                                              "@id = 'Section0000.xhtml' and @media-type = 'application/xhtml+xml']")), 1)
        self.assertEqual(len(self._xpath(opf, "/opf:package/opf:manifest/opf:item[@href = 'Text/Section0001.xhtml' and "
                                              "@id = 'Section0001.xhtml' and @media-type = 'application/xhtml+xml']")), 1)

        self.assertEqual(len(self._xpath(opf, "/opf:package/opf:spine[@toc = 'ncx']")), 1)
        self.assertEqual(len(self._xpath(opf, "/opf:package/opf:spine/opf:itemref[@idref = 'Section0000.xhtml']")), 1)
        self.assertEqual(len(self._xpath(opf, "/opf:package/opf:spine/opf:itemref[@idref = 'Section0000.xhtml']")), 1)
        self.assertEqual(len(self._xpath(opf, "/opf:package/opf:spine/opf:itemref[@idref = 'Section0001.xhtml']")), 1)

    def test_opf_metadata(self):
        self._epub.addTitle("Título del libro")
        self._epub.addLanguage("es")
        self._epub.addPublisher("La editorial")
        self._epub.addPublicationDate(datetime.date(2013, 5, 9))
        self._epub.addDescription("Esta es la descripción del ebook.")
        self._epub.addTranslator("Edgar Allan Poe", "Poe, Edgar Allan")
        self._epub.addAuthor("Jorge Luis Borges", "Borges, Jorge Luis")
        self._epub.addIlustrator("Vincent Van Gogh", "Van Gogh, Vincent")
        self._epub.addCustomMetadata("cover", "cover.jpg")

        self._generateEpub()

        opf = self._getOpf()

        self.assertEqual(len(self._xpath(opf, "/opf:package/opf:metadata/dc:identifier[@id = 'BookId' and @opf:scheme]")), 1)
        self.assertEqual(self._xpath(opf, "/opf:package/opf:metadata/dc:date[@opf:event = 'modification']/text()")[0],
                         datetime.datetime.now().strftime("%Y-%m-%d"))
        self.assertEqual(self._xpath(opf, "/opf:package/opf:metadata/dc:date[@opf:event = 'publication']/text()")[0], "2013-05-09")
        self.assertEqual(self._xpath(opf, "/opf:package/opf:metadata/dc:title/text()")[0], "Título del libro")
        self.assertEqual(self._xpath(opf, "/opf:package/opf:metadata/dc:language/text()")[0], "es")
        self.assertEqual(self._xpath(opf, "/opf:package/opf:metadata/dc:publisher/text()")[0], "La editorial")
        self.assertEqual(self._xpath(opf, "/opf:package/opf:metadata/dc:description/text()")[0], "Esta es la descripción del ebook.")
        self.assertEqual(self._xpath(opf, "/opf:package/opf:metadata/dc:contributor[@opf:role = 'trl' and "
                                          "@opf:file-as = 'Poe, Edgar Allan']/text()")[0], "Edgar Allan Poe")
        self.assertEqual(self._xpath(opf, "/opf:package/opf:metadata/dc:creator[@opf:role = 'aut' and "
                                          "@opf:file-as = 'Borges, Jorge Luis']/text()")[0], "Jorge Luis Borges")
        self.assertEqual(self._xpath(opf, "/opf:package/opf:metadata/dc:contributor[@opf:role = 'ill' and "
                                          "@opf:file-as = 'Van Gogh, Vincent']/text()")[0], "Vincent Van Gogh")
        self.assertEqual(len(self._xpath(opf, "/opf:package/opf:metadata/opf:meta[@name = 'cover' and @content = 'cover.jpg']")), 1)

    def test_toc_head_and_metadata(self):
        self._epub.addTitle("Título del libro")

        self._generateEpub()

        toc = self._getToc()
        opf = etree.XML(self._resultingEpub.read("OEBPS/content.opf"))

        self.assertEqual(len(self._xpath(toc, "/toc:ncx[@version = '2005-1']")), 1)

        opfUid = self._xpath(opf, "/opf:package/opf:metadata/dc:identifier/text()")[0]
        self.assertEqual(self._xpath(toc, "/toc:ncx/toc:head/toc:meta[@name = 'dtb:uid']/@content")[0], opfUid)

        self.assertEqual(len(self._xpath(toc, "/toc:ncx/toc:head/toc:meta[@name = 'dtb:depth' and @content = '1']")), 1)
        self.assertEqual(len(self._xpath(toc, "/toc:ncx/toc:head/toc:meta[@name = 'dtb:totalPageCount' and @content = '0']")), 1)
        self.assertEqual(len(self._xpath(toc, "/toc:ncx/toc:head/toc:meta[@name = 'dtb:maxPageNumber' and @content = '0']")), 1)

    def test_toc_nav_points_nested(self):
        nv1 = self._epub.addNavPoint("s1", "t1")
        nv1.addNavPoint("s2", "t2")
        nv1.addNavPoint("s3", "t3")

        nv2 = self._epub.addNavPoint("s4", "t4")
        nv21 = nv2.addNavPoint("s5", "t5")
        nv211 = nv21.addNavPoint("s6", "t6")
        nv211.addNavPoint("s7", "t7")

        nv3 = self._epub.addNavPoint("s8", "t8")
        nv31 = nv3.addNavPoint("s9", "t9")
        nv31.addNavPoint("s10", "t10")

        self._generateEpub()

        toc = self._getToc()

        self.assertEqual(len(self._xpath(toc, "/toc:ncx/toc:navMap/toc:navPoint[@id = 'navPoint-1' and @playOrder = '1']")), 1)
        self.assertEqual(len(self._xpath(toc, "/toc:ncx/toc:navMap/toc:navPoint[@id = 'navPoint-1']"
                                              "/toc:navPoint[@id = 'navPoint-2' and @playOrder = '2']")), 1)
        self.assertEqual(len(self._xpath(toc, "/toc:ncx/toc:navMap/toc:navPoint[@id = 'navPoint-1']"
                                              "/toc:navPoint[@id = 'navPoint-3' and @playOrder = '3']")), 1)
        self.assertEqual(len(self._xpath(toc, "/toc:ncx/toc:navMap/toc:navPoint[@id = 'navPoint-4' and @playOrder = '4']")), 1)
        self.assertEqual(len(self._xpath(toc, "/toc:ncx/toc:navMap/toc:navPoint[@id = 'navPoint-4']"
                                              "/toc:navPoint[@id = 'navPoint-5' and @playOrder = '5']")), 1)
        self.assertEqual(len(self._xpath(toc, "/toc:ncx/toc:navMap//toc:navPoint[@id = 'navPoint-5']"
                                              "/toc:navPoint[@id = 'navPoint-6' and @playOrder = '6']")), 1)
        self.assertEqual(len(self._xpath(toc, "/toc:ncx//toc:navPoint[@id = 'navPoint-6']"
                                              "/toc:navPoint[@id = 'navPoint-7' and @playOrder = '7']")), 1)
        self.assertEqual(len(self._xpath(toc, "/toc:ncx/toc:navMap/toc:navPoint[@id = 'navPoint-8' and @playOrder = '8']")), 1)
        self.assertEqual(len(self._xpath(toc, "/toc:ncx/toc:navMap/toc:navPoint[@id = 'navPoint-8']"
                                              "/toc:navPoint[@id = 'navPoint-9' and @playOrder = '9']")), 1)
        self.assertEqual(len(self._xpath(toc, "/toc:ncx/toc:navMap//toc:navPoint[@id = 'navPoint-9']"
                                              "/toc:navPoint[@id = 'navPoint-10' and @playOrder = '10']")), 1)

    def test_adding_images_and_css(self):
        self._epub.addImageData("image1.jpg", "blabla")
        self._epub.addImageData("image2.jpg", "blabla")
        self._epub.addImageData("image3.png", "blabla")
        self._epub.addImageData("image4.png", "blabla")
        self._epub.addStyleData("style.css", "content of style.css")

        self._generateEpub()
        opf = self._getOpf()

        self.assertEqual(len(self._xpath(opf, "/opf:package/opf:manifest/opf:item[@href = 'Images/image1.jpg' and "
                                              "@id = 'image1.jpg' and @media-type = 'image/jpeg']")), 1)
        self.assertEqual(len(self._xpath(opf, "/opf:package/opf:manifest/opf:item[@href = 'Images/image2.jpg' and "
                                              "@id = 'image2.jpg' and @media-type = 'image/jpeg']")), 1)
        self.assertEqual(len(self._xpath(opf, "/opf:package/opf:manifest/opf:item[@href = 'Images/image3.png' and "
                                              "@id = 'image3.png' and @media-type = 'image/png']")), 1)
        self.assertEqual(len(self._xpath(opf, "/opf:package/opf:manifest/opf:item[@href = 'Images/image4.png' and "
                                              "@id = 'image4.png' and @media-type = 'image/png']")), 1)
        self.assertEqual(len(self._xpath(opf, "/opf:package/opf:manifest/opf:item[@href = 'Styles/style.css' and "
                                              "@id = 'style.css' and @media-type = 'text/css']")), 1)

    def test_adding_file_to_metainf_directory(self):
        self._epub.addMetaFile("file.xml", "file content")

        self._generateEpub()

        try:
            self._resultingEpub.getinfo("META-INF/file.xml")
        except KeyError as e:
            self.fail(e)

    def test_opf_guide(self):
        self._epub.addReference("cubierta.xhtml", "Cover", "cover")

        self._generateEpub()
        opf = self._getOpf()

        self.assertEqual(len(self._xpath(opf, "/opf:package/opf:guide/opf:reference[@href = 'Text/cubierta.xhtml' and "
                                              "@title = 'Cover' and @type = 'cover']")), 1)

    def _printToc(self):
        print(self._resultingEpub.read("OEBPS/toc.ncx").decode("utf-8"))

    def _printOpf(self):
        print(self._resultingEpub.read("OEBPS/content.opf").decode("utf-8"))

    def _getToc(self):
        try:
            return etree.XML(self._resultingEpub.read("OEBPS/toc.ncx"))
        except KeyError as e:
            self.fail(e)

    def _getOpf(self):
        try:
            return etree.XML(self._resultingEpub.read("OEBPS/content.opf"))
        except KeyError as e:
            self.fail(e)

    def _xpath(self, element, xpath):
        return element.xpath(xpath, namespaces=EpubWriterTests._NAMESPACES)

    def _generateEpub(self):
        self._epub.generate(self._outputFile)
        self._resultingEpub = zipfile.ZipFile(self._outputFile)


class EpubValidationTests(unittest.TestCase):
    _EPUBCHECK_PATH = os.path.join(os.path.dirname(__file__), "epubcheck-3.0.1", "epubcheck-3.0.1.jar")
    _SAMPLE_HTML_CONTENT = ('<?xml version="1.0" encoding="utf-8"?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" '
                            '"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"><html xmlns="http://www.w3.org/1999/xhtml">'
                            '<head><title></title></head><body><p>&nbsp;</p></body></html>')

    def setUp(self):
        self._outputFile = tempfile.NamedTemporaryFile(suffix=".epub", delete=False)
        self._epub = pyepub.pyepubwriter.epub.EpubWriter()
        self._epub.addTitle("Título del libro")
        self._epub.addLanguage("es")

    def tearDown(self):
        self._outputFile.close()
        os.remove(self._outputFile.name)

    def test_simple_epub(self):
        self._epub.addHtmlData("s1.xhtml", EpubValidationTests._SAMPLE_HTML_CONTENT)
        self._epub.addNavPoint("s1.xhtml", "Título del libro")

        self._generateEpub()
        self._validateEpub()

    def _generateEpub(self):
        self._epub.generate(self._outputFile)

    def _validateEpub(self):
        epubChecker = subprocess.Popen(["java", "-jar", self._EPUBCHECK_PATH, self._outputFile.name],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = epubChecker.communicate()

        if "No errors or warnings detected." not in str(out):
            self.fail(err.decode("utf-8").strip())


if __name__ == "__main__":
    unittest.main()