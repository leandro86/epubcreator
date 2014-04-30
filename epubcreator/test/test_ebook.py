import unittest
import tempfile
import datetime
import io

from lxml import etree
from PIL import Image

from epubcreator.pyepub.pyepubreader import epub
from epubcreator.epubbase import ebook, ebook_data, ebook_metadata, images


class SynopsisTest(unittest.TestCase):
    _DEFAULT_SYNOPSIS = ("Yo por bien tengo que cosas tan señaladas, y por ventura nunca oídas ni vistas, vengan a noticia de muchos y no se "
                         "entierren en la sepultura del olvido, pues podría ser que alguno que las lea halle algo que le agrade, y a los que "
                         "no ahondaren tanto los deleite."
                         "Y a este propósito dice Plinio que no hay libro, por malo que sea, que no tenga alguna cosa buena; mayormente que "
                         "los gustos no son todos unos, mas lo que uno no come, otro se pierde por ello. LÁZARO DE TORMES.")

    def setUp(self):
        self._common = Common()

    def tearDown(self):
        self._common.release()

    def test_synopsis_file_exists(self):
        self._common.metadata.synopsis = ""

        self._common.generateEbook()

        self.assertTrue(self._common.outputEpub.hasFile("sinopsis.xhtml"))

    def test_default_synopsis(self):
        self._common.metadata.synopsis = ""

        self._common.generateEbook()

        synopsis = self._getSynopsisFile()

        self.assertEqual(self._common.xpath(synopsis, "count(//x:p)"), 2)

        gotSynopsis = "".join(self._common.xpath(synopsis, "x:body/x:div[@class = 'sinopsis']/x:p[1][@class = 'salto10']//text()"))
        gotSynopsis += "".join(self._common.xpath(synopsis, "x:body/x:div[@class = 'sinopsis']/x:p[2]//text()"))

        self.assertEqual(gotSynopsis, SynopsisTest._DEFAULT_SYNOPSIS)

    def test_synopsis(self):
        self._common.metadata.synopsis = "Párrafo 1.\nPárrafo 2.\nPárrafo 3."

        self._common.generateEbook()

        synopsis = self._getSynopsisFile()

        self.assertEqual(self._common.xpath(synopsis, "count(//x:p)"), 3)

        self.assertEqual(self._common.xpath(synopsis, "x:body/x:div[@class = 'sinopsis']/x:p[1][@class = 'salto10']/text()")[0], "Párrafo 1.")
        self.assertEqual(self._common.xpath(synopsis, "x:body/x:div[@class = 'sinopsis']/x:p[2]/text()")[0], "Párrafo 2.")
        self.assertEqual(self._common.xpath(synopsis, "x:body/x:div[@class = 'sinopsis']/x:p[3]/text()")[0], "Párrafo 3.")

    def test_tags_are_preserved_in_synopsis(self):
        self._common.metadata.synopsis = "Párrafo 1.\n<strong>Párrafo <em>2</em></strong>.\n<span>Párrafo 3.</span>"

        self._common.generateEbook()

        synopsis = self._getSynopsisFile()

        self.assertEqual(self._common.xpath(synopsis, "count(//x:p)"), 3)

        self.assertEqual(self._common.xpath(synopsis, "x:body/x:div[@class = 'sinopsis']/x:p[1][@class = 'salto10']/text()")[0], "Párrafo 1.")
        self.assertEqual(self._common.xpath(synopsis, "x:body/x:div[@class = 'sinopsis']/x:p[2]//text()"), ["Párrafo ", "2", "."])
        self.assertEqual(self._common.xpath(synopsis, "x:body/x:div[@class = 'sinopsis']/x:p[3]//text()"), ["Párrafo 3."])

    def _getSynopsisFile(self):
        return etree.parse(self._common.outputEpub.open("OEBPS/Text/{0}".format("sinopsis.xhtml")))


class TitleTest(unittest.TestCase):
    def setUp(self):
        self._common = Common()

    def tearDown(self):
        self._common.release()

    def test_title_file_exists(self):
        self._common.generateEbook()

        self.assertTrue(self._common.outputEpub.hasFile("titulo.xhtml"))

    def test_default_author(self):
        self._common.metadata.authors.clear()

        self._common.generateEbook()

        title = self._getTitleFile()

        self.assertEqual(self._common.xpath(title, "x:body/x:p[@class = 'tautor']/text()")[0], "Autor")

    def test_single_author(self):
        self._common.metadata.authors.append(ebook_metadata.Person("Jorge Luis Borges", "bla"))

        self._common.generateEbook()

        title = self._getTitleFile()

        self.assertEqual(self._common.xpath(title, "x:body/x:p[@class = 'tautor']/text()")[0], "Jorge Luis Borges")

    def test_multiple_authors(self):
        self._common.metadata.authors.append(ebook_metadata.Person("Jorge Luis Borges", "bla"))
        self._common.metadata.authors.append(ebook_metadata.Person("Edgar Allan Poe", "bla"))
        self._common.metadata.authors.append(ebook_metadata.Person("William Shakespeare", "bla"))
        self._common.metadata.authors.append(ebook_metadata.Person("H. P. Lovecraft", "bla"))

        self._common.generateEbook()

        title = self._getTitleFile()

        self.assertEqual(self._common.xpath(title, "x:body/x:p[@class = 'tautor']/text()")[0],
                         "Jorge Luis Borges & Edgar Allan Poe & William Shakespeare & H. P. Lovecraft")

    def test_default_title(self):
        self._common.metadata.title = ""

        self._common.generateEbook()

        title = self._getTitleFile()

        self.assertEqual(self._common.xpath(title, "x:body/x:h1[@class = 'ttitulo']/text()")[0], "Título")

    def test_title(self):
        self._common.metadata.title = "Título del libro"

        self._common.generateEbook()

        title = self._getTitleFile()

        self.assertEqual(self._common.xpath(title, "x:body/x:h1[@class = 'ttitulo']/text()")[0], "Título del libro")

    def test_subtitle(self):
        self._common.metadata.subtitle = "Subtítulo del libro"

        self._common.generateEbook()

        title = self._getTitleFile()

        self.assertEqual(self._common.xpath(title, "x:body/x:p[@class = 'tsubtitulo']/text()")[0], "Subtítulo del libro")

    def test_not_subtitle(self):
        self._common.metadata.subtitle = ""

        self._common.generateEbook()

        title = self._getTitleFile()

        self.assertFalse(self._common.xpath(title, "x:body/x:p[@class = 'tsubtitulo']/text()"))
        # En titulo.xhtml hay un comentario indicando en el campo de subtítulo que es opcional, por eso debo verificar
        # que también ese comentario se haya borrado.
        self.assertFalse(self._common.xpath(title, "x:body/comment()"))

    def test_revision(self):
        self._common.generateEbook()

        title = self._getTitleFile()

        self.assertEqual(self._common.xpath(title, "x:body/x:p[@class = 'trevision']/text()")[0], "ePub r1.0")

    def test_default_editor(self):
        self._common.metadata.editor = ""

        self._common.generateEbook()

        title = self._getTitleFile()

        self.assertEqual(self._common.xpath(title, "x:body/x:p[@class = 'tfirma']/text()")[0], "Editor ")

    def test_editor(self):
        self._common.metadata.editor = "El editor"

        self._common.generateEbook()

        title = self._getTitleFile()

        self.assertEqual(self._common.xpath(title, "x:body/x:p[@class = 'tfirma']/text()")[0], "El editor ")

    def test_modification_date(self):
        self._common.generateEbook()

        title = self._getTitleFile()

        self.assertEqual(self._common.xpath(title, "x:body/x:p[@class = 'tfirma']/x:span[@class = 'tfecha']/text()")[0],
                         datetime.datetime.now().strftime("%d.%m.%y"))

    def test_collection(self):
        self._common.metadata.collectionName = "La saga"
        self._common.metadata.subCollectionName = "La serie"
        self._common.metadata.collectionVolume = "2"

        self._common.generateEbook()

        title = self._getTitleFile()

        self.assertEqual(self._common.xpath(title, "x:body/x:p[@class = 'tsubtitulo']/text()")[0], "La saga: La serie - 2")

    def test_subcollection_only(self):
        self._common.metadata.subCollectionName = "La serie"
        self._common.metadata.collectionVolume = "2"

        self._common.generateEbook()

        title = self._getTitleFile()

        self.assertEqual(self._common.xpath(title, "x:body/x:p[@class = 'tsubtitulo']/text()")[0], "La serie - 2")

    def _getTitleFile(self):
        return etree.parse(self._common.outputEpub.open("OEBPS/Text/{0}".format("titulo.xhtml")))


class InfoTest(unittest.TestCase):
    def setUp(self):
        self._common = Common()

    def tearDown(self):
        self._common.release()

    def test_info_file_exists(self):
        self._common.generateEbook()

        self.assertTrue(self._common.outputEpub.hasFile("info.xhtml"))

    def test_original_title(self):
        self._common.metadata.originalTitle = "El título original"

        self._common.generateEbook()

        info = self._getInfoFile()

        # El título en el campo "Título original" se encuentra dentro de un tag "em".
        self.assertEqual(self._common.xpath(info, "x:body/x:div[@class = 'info']/x:p[1]//text()"), ["Título original: ", "El título original"])

    def test_not_original_title(self):
        self._common.metadata.originalTitle = ""

        self._common.generateEbook()

        info = self._getInfoFile()

        self.assertFalse(self._common.xpath(info, "x:body/x:div[@class = 'info']/x:p[starts-with(text(), 'Título original')]"))

    def test_default_author(self):
        self._common.metadata.authors.clear()

        self._common.generateEbook()

        info = self._getInfoFile()

        self.assertEqual(self._common.xpath(info, "x:body/x:div[@class = 'info']/x:p[1]/text()")[0], "Autor")

    def test_single_author(self):
        self._common.metadata.authors.append(ebook_metadata.Person("Jorge Luis Borges", "bla"))

        self._common.generateEbook()

        info = self._getInfoFile()

        self.assertEqual(self._common.xpath(info, "x:body/x:div[@class = 'info']/x:p[1]/text()")[0], "Jorge Luis Borges")

    def test_multiple_authors(self):
        self._common.metadata.authors.append(ebook_metadata.Person("Jorge Luis Borges", "bla"))
        self._common.metadata.authors.append(ebook_metadata.Person("Edgar Allan Poe", "bla"))
        self._common.metadata.authors.append(ebook_metadata.Person("William Shakespeare", "bla"))
        self._common.metadata.authors.append(ebook_metadata.Person("H. P. Lovecraft", "bla"))

        self._common.generateEbook()

        info = self._getInfoFile()

        self.assertEqual(self._common.xpath(info, "x:body/x:div[@class = 'info']/x:p[1]/text()")[0],
                         "Jorge Luis Borges & Edgar Allan Poe & William Shakespeare & H. P. Lovecraft")

    def test_publication_date(self):
        self._common.metadata.publicationDate = datetime.date(1756, 5, 9)

        self._common.generateEbook()

        info = self._getInfoFile()

        # Antes de la coma viene el nombre del autor, que siempre va a estar.
        self.assertTrue(self._common.xpath(info, "x:body/x:div[@class = 'info']/x:p[1]/text()")[0].endswith(", 1756"))

    def test_not_publication_date(self):
        self._common.metadata.publicationDate = None

        self._common.generateEbook()

        info = self._getInfoFile()

        # La fecha de publicación en el idioma original se coloca en el mismo párrafo, junto con el
        # autor, y separada por una coma.
        self.assertFalse("," in self._common.xpath(info, "x:body/x:div[@class = 'info']/x:p[1]/text()")[0])

    def test_single_translator(self):
        self._common.metadata.translators.append(ebook_metadata.Person("Jorge Luis Borges", "bla"))

        self._common.generateEbook()

        info = self._getInfoFile()

        self.assertEqual(self._common.xpath(info, "x:body/x:div[@class = 'info']/x:p[2]/text()")[0], "Traducción: Jorge Luis Borges")

    def test_multiple_translators(self):
        self._common.metadata.translators.append(ebook_metadata.Person("Jorge Luis Borges", "bla"))
        self._common.metadata.translators.append(ebook_metadata.Person("Edgar Allan Poe", "bla"))
        self._common.metadata.translators.append(ebook_metadata.Person("William Shakespeare", "bla"))
        self._common.metadata.translators.append(ebook_metadata.Person("H. P. Lovecraft", "bla"))

        self._common.generateEbook()

        info = self._getInfoFile()

        self.assertEqual(self._common.xpath(info, "x:body/x:div[@class = 'info']/x:p[2]/text()")[0],
                         "Traducción: Jorge Luis Borges & Edgar Allan Poe & William Shakespeare & H. P. Lovecraft")

    def test_not_translator(self):
        self._common.metadata.translators.clear()

        self._common.generateEbook()

        info = self._getInfoFile()

        self.assertFalse(self._common.xpath(info, "x:body/x:div[@class = 'info']/x:p[starts-with(text(), 'Traducción')]"))

    def test_single_ilustrator(self):
        self._common.metadata.ilustrators.append(ebook_metadata.Person("Jorge Luis Borges", "bla"))

        self._common.generateEbook()

        info = self._getInfoFile()

        self.assertEqual(self._common.xpath(info, "x:body/x:div[@class = 'info']/x:p[2]/text()")[0], "Ilustraciones: Jorge Luis Borges")

    def test_multiple_ilustrators(self):
        self._common.metadata.ilustrators.append(ebook_metadata.Person("Jorge Luis Borges", "bla"))
        self._common.metadata.ilustrators.append(ebook_metadata.Person("Edgar Allan Poe", "bla"))
        self._common.metadata.ilustrators.append(ebook_metadata.Person("William Shakespeare", "bla"))
        self._common.metadata.ilustrators.append(ebook_metadata.Person("H. P. Lovecraft", "bla"))

        self._common.generateEbook()

        info = self._getInfoFile()

        self.assertEqual(self._common.xpath(info, "x:body/x:div[@class = 'info']/x:p[2]/text()")[0],
                         "Ilustraciones: Jorge Luis Borges & Edgar Allan Poe & William Shakespeare & H. P. Lovecraft")

    def test_not_ilustrator(self):
        self._common.metadata.ilustrators.clear()

        self._common.generateEbook()

        info = self._getInfoFile()

        self.assertFalse(self._common.xpath(info, "x:body/x:div[@class = 'info']/x:p[starts-with(text(), 'Ilustraciones')]"))

    def test_default_cover_modification(self):
        self._common.metadata.coverDesigner = "bla"
        self._common.metadata.coverModification = ""

        self._common.generateEbook()

        info = self._getInfoFile()

        self.assertTrue(self._common.xpath(info, "x:body/x:div[@class = 'info']/x:p[2]/text()")[0].startswith("Diseño de cubierta: "))

    def test_cover_modification(self):
        self._common.metadata.coverDesigner = "bla"
        self._common.metadata.coverModification = "Retoque"

        self._common.generateEbook()

        info = self._getInfoFile()

        self.assertTrue(self._common.xpath(info, "x:body/x:div[@class = 'info']/x:p[2]/text()")[0].startswith("Retoque de cubierta: "))

    def test_not_cover_modification(self):
        self._common.metadata.coverDesigner = ""

        self._common.generateEbook()

        info = self._getInfoFile()

        self.assertFalse(self._common.xpath(info, "x:body/x:div[@class = 'info']/x:p[starts-with(text(), 'Diseño de cubierta')]"))
        self.assertFalse(any("si la cubierta fue creada" in x.text for x in self._common.xpath(info, "x:body/x:div[@class = 'info']/comment()")))

    def test_default_editor(self):
        self._common.metadata.editor = ""

        self._common.generateEbook()

        info = self._getInfoFile()

        self.assertEqual(self._common.xpath(info, "x:body/x:div[@class = 'info']/x:p[2]/text()")[0], "Editor digital: Editor")

    def test_editor(self):
        self._common.metadata.editor = "El editor"

        self._common.generateEbook()

        info = self._getInfoFile()

        self.assertEqual(self._common.xpath(info, "x:body/x:div[@class = 'info']/x:p[2]/text()")[0], "Editor digital: El editor")

    def test_epub_base_revision(self):
        self._common.generateEbook()

        info = self._getInfoFile()

        self.assertEqual(self._common.xpath(info, "x:body/x:div[@class = 'info']/x:p[3]/text()")[0], "ePub base r1.1")

    def _getInfoFile(self):
        return etree.parse(self._common.outputEpub.open("OEBPS/Text/{0}".format("info.xhtml")))


class DedicationTest(unittest.TestCase):
    DEFAULT_DEDICATION = ("Suspiró entonces mío Cid, de pesadumbre cargado, y comenzó a hablar así, justamente mesurado: «¡Loado "
                          "seas, Señor, Padre que estás en lo alto! Todo esto me han urdido mis enemigos malvados».ANÓNIMO")

    def setUp(self):
        self._common = Common()

    def tearDown(self):
        self._common.release()

    def test_dedication(self):
        self._common.metadata.dedication = "Párrafo 1.\nPárrafo 2.\nPárrafo 3."

        self._common.generateEbook()

        dedication = self._getDedicationFile()

        self.assertEqual(self._common.xpath(dedication, "count(//x:p)"), 3)

        self.assertEqual(self._common.xpath(dedication, "x:body/x:div[@class = 'dedicatoria']/x:p[1]/text()")[0], "Párrafo 1.")
        self.assertEqual(self._common.xpath(dedication, "x:body/x:div[@class = 'dedicatoria']/x:p[2]/text()")[0], "Párrafo 2.")
        self.assertEqual(self._common.xpath(dedication, "x:body/x:div[@class = 'dedicatoria']/x:p[3]/text()")[0], "Párrafo 3.")

    def test_tags_are_preserved_in_dedication(self):
        self._common.metadata.dedication = "Párrafo 1.\n<strong>Párrafo <em>2</em></strong>.\n<span>Párrafo 3.</span>"

        self._common.generateEbook()

        dedication = self._getDedicationFile()

        self.assertEqual(self._common.xpath(dedication, "count(//x:p)"), 3)

        self.assertEqual(self._common.xpath(dedication, "x:body/x:div[@class = 'dedicatoria']/x:p[1]/text()")[0], "Párrafo 1.")
        self.assertEqual(self._common.xpath(dedication, "x:body/x:div[@class = 'dedicatoria']/x:p[2]//text()"), ["Párrafo ", "2", "."])
        self.assertEqual(self._common.xpath(dedication, "x:body/x:div[@class = 'dedicatoria']/x:p[3]//text()"), ["Párrafo 3."])

    def test_not_dedication(self):
        self._common.metadata.dedication = ""

        self._common.generateEbook(includeOptionalFiles=False)

        self.assertFalse(self._common.outputEpub.hasFile("dedicatoria.xhtml"))

    def test_dedication_exists_when_not_include_optional_files(self):
        self._common.metadata.dedication = "bla"

        self._common.generateEbook(includeOptionalFiles=False)

        self.assertTrue(self._common.outputEpub.hasFile("dedicatoria.xhtml"))

    def test_default_dedication(self):
        self._common.metadata.dedication = ""

        self._common.generateEbook()

        dedication = self._getDedicationFile()

        self.assertEqual(self._common.xpath(dedication, "count(//x:p)"), 2)

        gotDedication = "".join(self._common.xpath(dedication, "x:body/x:div[@class = 'dedicatoria']/x:p[1]//text()"))
        gotDedication += "".join(self._common.xpath(dedication, "x:body/x:div[@class = 'dedicatoria']/x:p[2]//text()"))

        wantDedication = DedicationTest.DEFAULT_DEDICATION

        self.assertEqual(gotDedication, wantDedication)

    def _getDedicationFile(self):
        return etree.parse(self._common.outputEpub.open("OEBPS/Text/{0}".format("dedicatoria.xhtml")))


class AuthorTest(unittest.TestCase):
    _AUTHOR_BIOGRAPHY = ("NOMBRE DEL AUTOR (Reikiavik, Islandia, 2013 - Terra III, 3072). Lorem ipsum dolor sit amet, consectetur "
                         "adipiscing elit. Nunc vel libero sed est ultrices elementum at vel lacus. Sed laoreet, velit nec congue "
                         "pellentesque, quam urna pretium nunc, et ultrices nulla lacus non libero."
                         "Integer eu leo justo, vel sodales arcu. Donec posuere nunc in lectus laoreet a rhoncus enim fermentum. Nunc "
                         "luctus accumsan ligula eu molestie.")

    def setUp(self):
        self._common = Common()

    def tearDown(self):
        self._common.release()

    def test_only_one_author_file_exists_when_no_authors_but_include_optional_files(self):
        self._common.metadata.authors.clear()

        self._common.generateEbook()

        authors = [a[0] for a in self._getAuthorFiles()]

        self.assertEqual(len(authors), 1)
        self.assertEqual(authors[0], "autor.xhtml")

    def test_only_one_author_file_exists_when_author_has_no_data_but_include_optional_files(self):
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla"))

        self._common.generateEbook()

        authors = [a[0] for a in self._getAuthorFiles()]

        self.assertEqual(len(authors), 1)
        self.assertEqual(authors[0], "autor.xhtml")

    def test_two_author_files_exist_when_both_authors_have_no_data_but_include_optional_files(self):
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla"))
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla"))

        self._common.generateEbook()

        authors = [a[0] for a in self._getAuthorFiles()]

        self.assertEqual(len(authors), 2)
        self.assertTrue("autor.xhtml" in authors and "autor1.xhtml" in authors)

    def test_no_author_file_exist_when_no_authors_and_not_include_optional_files(self):
        self._common.metadata.authors.clear()

        self._common.generateEbook(includeOptionalFiles=False)

        authors = self._getAuthorFiles()

        self.assertFalse(authors)

    def test_default_author_biography(self):
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla"))

        self._common.generateEbook()

        author = self._getAuthorFiles()[0][1]

        self.assertEqual(self._common.xpath(author, "count(//x:p)"), 2)

        gotAuthorBiography = "".join(self._common.xpath(author, "x:body/x:div[@class = 'autor']/x:p[1]//text()"))
        gotAuthorBiography += "".join(self._common.xpath(author, "x:body/x:div[@class = 'autor']/x:p[2]//text()"))

        wantAuthorBiography = AuthorTest._AUTHOR_BIOGRAPHY

        self.assertEqual(gotAuthorBiography, wantAuthorBiography)

    def test_author_biography(self):
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla", biography="Párrafo 1.\nPárrafo 2.\nPárrafo 3."))

        self._common.generateEbook()

        author = self._getAuthorFiles()[0][1]

        self.assertEqual(self._common.xpath(author, "/x:html/x:body/x:div[@class = 'autor']/x:p[position() = 1]/text()")[0], "Párrafo 1.")
        self.assertEqual(self._common.xpath(author, "/x:html/x:body/x:div[@class = 'autor']/x:p[position() = 2]/text()")[0], "Párrafo 2.")
        self.assertEqual(self._common.xpath(author, "/x:html/x:body/x:div[@class = 'autor']/x:p[position() = 3]/text()")[0], "Párrafo 3.")

    def test_tags_are_preserved_in_author_biography(self):
        biography = "Párrafo 1.\n<strong>Párrafo <em>2</em></strong>.\n<span>Párrafo 3.</span>"
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla", biography=biography))

        self._common.generateEbook()

        author = self._getAuthorFiles()[0][1]

        self.assertEqual(self._common.xpath(author, "count(//x:p)"), 3)

        self.assertEqual(self._common.xpath(author, "x:body/x:div[@class = 'autor']/x:p[1]/text()")[0], "Párrafo 1.")
        self.assertEqual(self._common.xpath(author, "x:body/x:div[@class = 'autor']/x:p[2]//text()"), ["Párrafo ", "2", "."])
        self.assertEqual(self._common.xpath(author, "x:body/x:div[@class = 'autor']/x:p[3]//text()"), ["Párrafo 3."])

    def test_author_biography_when_custom_image(self):
        image = Image.new("RGB", (320, 400))
        buffer = io.BytesIO()
        image.save(buffer, "JPEG")

        self._common.metadata.authors.append(ebook_metadata.Person("bla",
                                                                   "bla",
                                                                   biography="Párrafo 1.",
                                                                   image=images.AuthorImage(buffer.getvalue(), allowProcessing=False)))

        self._common.generateEbook()

        author = self._getAuthorFiles()[0][1]

        self.assertEqual(self._common.xpath(author, "count(//x:p)"), 1)
        self.assertEqual(self._common.xpath(author, "/x:html/x:body/x:div[@class = 'autor']/x:p[position() = 1]/text()")[0], "Párrafo 1.")

    def test_author_header_title_with_male_author(self):
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla"))

        self._common.generateEbook()

        author = self._getAuthorFiles()[0][1]

        self.assertEqual(len(self._common.xpath(author, "//x:h1")), 1)
        self.assertEqual(self._common.xpath(author, "x:body/x:h1[@class = 'oculto']/@title")[0], "Autor")

    def test_author_header_title_with_female_author(self):
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla", ebook_metadata.Person.FEMALE_GENDER))

        self._common.generateEbook()

        author = self._getAuthorFiles()[0][1]

        self.assertEqual(len(self._common.xpath(author, "//x:h1")), 1)
        self.assertEqual(self._common.xpath(author, "x:body/x:h1[@class = 'oculto']/@title")[0], "Autora")

    def test_author_header_title_with_two_authors(self):
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla", ebook_metadata.Person.MALE_GENDER))
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla", ebook_metadata.Person.FEMALE_GENDER))

        self._common.generateEbook()

        firstAuthor = next(a[1] for a in self._getAuthorFiles() if a[0] == "autor.xhtml")

        self.assertEqual(len(self._common.xpath(firstAuthor, "//x:h1")), 1)
        self.assertEqual(self._common.xpath(firstAuthor, "x:body/x:h1[@class = 'oculto']/@title")[0], "Autores")

    def test_only_first_author_file_has_header_when_two_author_files(self):
        image = Image.new("RGB", (320, 400))
        buffer = io.BytesIO()
        image.save(buffer, "JPEG")

        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla", image=images.AuthorImage(buffer.getvalue(), allowProcessing=False)))
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla", image=images.AuthorImage(buffer.getvalue(), allowProcessing=False)))

        self._common.generateEbook()

        authors = self._getAuthorFiles()
        firstAuthor = next(a[1] for a in authors if a[0] == "autor.xhtml")
        secondAuthor = next(a[1] for a in authors if a[0] == "autor1.xhtml")

        self.assertEqual(len(self._common.xpath(firstAuthor, "//x:h1")), 1)
        self.assertFalse(self._common.xpath(secondAuthor, "//x:h1"))

    def test_image_reference_when_one_author_file(self):
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla"))

        self._common.generateEbook()

        author = self._getAuthorFiles()[0][1]

        self.assertTrue(self._common.xpath(author, "x:body/x:div[@class = 'vineta']/x:img/@src")[0].endswith("autor.jpg"))

    def test_image_reference_when_two_author_files(self):
        image = Image.new("RGB", (320, 400))
        buffer = io.BytesIO()
        image.save(buffer, "JPEG")

        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla", image=images.AuthorImage(buffer.getvalue(), allowProcessing=False)))
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla", image=images.AuthorImage(buffer.getvalue(), allowProcessing=False)))

        self._common.generateEbook()

        authors = self._getAuthorFiles()
        firstAuthor = next(a[1] for a in authors if a[0] == "autor.xhtml")
        secondAuthor = next(a[1] for a in authors if a[0] == "autor1.xhtml")

        self.assertTrue(self._common.xpath(firstAuthor, "x:body/x:div[@class = 'vineta']/x:img/@src")[0].endswith("autor.jpg"))
        self.assertTrue(self._common.xpath(secondAuthor, "x:body/x:div[@class = 'vineta']/x:img/@src")[0].endswith("autor1.jpg"))

    def test_author_file_is_last_in_play_order_when_epub_doesnt_have_notes(self):
        self._common.generateEbook()

        htmlFiles = self._common.outputEpub.getHtmlFileNamesReadingOrder()
        self.assertEqual(htmlFiles[-1], "autor.xhtml")

    def test_author_file_is_second_to_last_in_play_order_when_epub_contains_notes(self):
        ebookData = ebook_data.EbookData()
        ebookData.createNotesSection().save()

        self._common.generateEbook(ebookData)

        htmlFiles = self._common.outputEpub.getHtmlFileNamesReadingOrder()
        self.assertEqual(htmlFiles[-2], "autor.xhtml")

    def test_player_order_when_multiple_author_files(self):
        image = Image.new("RGB", (320, 400))
        buffer = io.BytesIO()
        image.save(buffer, "JPEG")

        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla", image=images.AuthorImage(buffer.getvalue(), allowProcessing=False)))
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla", image=images.AuthorImage(buffer.getvalue(), allowProcessing=False)))
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla", image=images.AuthorImage(buffer.getvalue(), allowProcessing=False)))
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla", image=images.AuthorImage(buffer.getvalue(), allowProcessing=False)))

        self._common.generateEbook()

        htmlFiles = self._common.outputEpub.getHtmlFileNamesReadingOrder()
        self.assertEqual(htmlFiles[-4:], ["autor.xhtml", "autor1.xhtml", "autor2.xhtml", "autor3.xhtml"])

    def _getAuthorFiles(self):
        authorFiles = []

        for authorFileName in (f for f in self._common.outputEpub.getNamelist() if f.startswith("autor") and f.endswith(".xhtml")):
            authorFiles.append((authorFileName, etree.parse(self._common.outputEpub.open("OEBPS/Text/{0}".format(authorFileName)))))

        return authorFiles


class MetadataTest(unittest.TestCase):
    def setUp(self):
        self._common = Common()

    def tearDown(self):
        self._common.release()

    def test_default_author(self):
        self._common.metadata.authors.clear()

        self._common.generateEbook()

        authors = self._common.outputEpub.getAuthors()
        self.assertEqual(len(authors), 1)
        self.assertEqual(authors[0], ("Autor", "Autor"))

    def test_one_author(self):
        self._common.metadata.authors.append(ebook_metadata.Person("Jorge Luis Borges", "Borges, Jorge Luis"))

        self._common.generateEbook()

        authors = self._common.outputEpub.getAuthors()
        self.assertEqual(len(authors), 1)
        self.assertEqual(authors[0], ("Jorge Luis Borges", "Borges, Jorge Luis"))

    def test_multiple_authors(self):
        self._common.metadata.authors.append(ebook_metadata.Person("Jorge Luis Borges", "Borges, Jorge Luis"))
        self._common.metadata.authors.append(ebook_metadata.Person("Edgar Allan Poe", "Poe, Edgar Allan"))
        self._common.metadata.authors.append(ebook_metadata.Person("William Shakespeare", "Shakespeare, William"))
        self._common.metadata.authors.append(ebook_metadata.Person("H. P. Lovecraft", "Lovecraft, H. P."))

        self._common.generateEbook()

        authors = self._common.outputEpub.getAuthors()
        self.assertEqual(len(authors), 1)
        self.assertEqual(authors[0], ("Jorge Luis Borges & Edgar Allan Poe & William Shakespeare & H. P. Lovecraft",
                                      "Borges, Jorge Luis & Poe, Edgar Allan & Shakespeare, William & Lovecraft, H. P."))

    def test_default_title(self):
        self._common.metadata.title = ""

        self._common.generateEbook()

        self.assertEqual(self._common.outputEpub.getTitle(), "Título")

    def test_title(self):
        self._common.metadata.title = "Título del libro"

        self._common.generateEbook()

        self.assertEqual(self._common.outputEpub.getTitle(), "Título del libro")

    def test_modification_date(self):
        self._common.generateEbook()

        self.assertEqual(self._common.outputEpub.getModificationDate(), datetime.datetime.now().strftime("%Y-%m-%d"))

    def test_publication_date(self):
        self._common.metadata.publicationDate = datetime.date(1756, 5, 9)

        self._common.generateEbook()

        self.assertEqual(self._common.outputEpub.getPublicationDate(), "1756-05-09")

    def test_not_publication_date(self):
        self._common.metadata.publicationDate = None

        self._common.generateEbook()

        self.assertIsNone(self._common.outputEpub.getPublicationDate())

    def test_one_translator(self):
        self._common.metadata.translators.append(ebook_metadata.Person("Jorge Luis Borges", "Borges, Jorge Luis"))

        self._common.generateEbook()

        translators = self._common.outputEpub.getTranslators()
        self.assertEqual(len(translators), 1)
        self.assertEqual(translators[0], ("Jorge Luis Borges", "Borges, Jorge Luis"))

    def test_multiple_translators(self):
        self._common.metadata.translators.append(ebook_metadata.Person("Jorge Luis Borges", "Borges, Jorge Luis"))
        self._common.metadata.translators.append(ebook_metadata.Person("Edgar Allan Poe", "Poe, Edgar Allan"))
        self._common.metadata.translators.append(ebook_metadata.Person("William Shakespeare", "Shakespeare, William"))
        self._common.metadata.translators.append(ebook_metadata.Person("H. P. Lovecraft", "Lovecraft, H. P."))

        self._common.generateEbook()

        translators = self._common.outputEpub.getTranslators()
        self.assertEqual(len(translators), 1)
        self.assertEqual(translators[0], ("Jorge Luis Borges & Edgar Allan Poe & William Shakespeare & H. P. Lovecraft",
                                          "Borges, Jorge Luis & Poe, Edgar Allan & Shakespeare, William & Lovecraft, H. P."))

    def test_not_translator(self):
        self._common.metadata.translators.clear()

        self._common.generateEbook()

        self.assertFalse(self._common.outputEpub.getTranslators())

    def test_one_ilustrator(self):
        self._common.metadata.ilustrators.append(ebook_metadata.Person("Jorge Luis Borges", "Borges, Jorge Luis"))

        self._common.generateEbook()

        ilustrators = self._common.outputEpub.getIlustrators()
        self.assertEqual(len(ilustrators), 1)
        self.assertEqual(ilustrators[0], ("Jorge Luis Borges", "Borges, Jorge Luis"))

    def test_multiple_ilustrators(self):
        self._common.metadata.ilustrators.append(ebook_metadata.Person("Jorge Luis Borges", "Borges, Jorge Luis"))
        self._common.metadata.ilustrators.append(ebook_metadata.Person("Edgar Allan Poe", "Poe, Edgar Allan"))
        self._common.metadata.ilustrators.append(ebook_metadata.Person("William Shakespeare", "Shakespeare, William"))
        self._common.metadata.ilustrators.append(ebook_metadata.Person("H. P. Lovecraft", "Lovecraft, H. P."))

        self._common.generateEbook()

        ilustrators = self._common.outputEpub.getIlustrators()
        self.assertEqual(len(ilustrators), 1)
        self.assertEqual(ilustrators[0], ("Jorge Luis Borges & Edgar Allan Poe & William Shakespeare & H. P. Lovecraft",
                                          "Borges, Jorge Luis & Poe, Edgar Allan & Shakespeare, William & Lovecraft, H. P."))

    def test_not_ilustrator(self):
        self._common.metadata.ilustrators.clear()

        self._common.generateEbook()

        self.assertFalse(self._common.outputEpub.getIlustrators())

    def test_default_synopsis(self):
        self._common.generateEbook()

        self.assertEqual(self._common.outputEpub.getDescription(), "Sinopsis")

    def test_synopsis(self):
        self._common.metadata.synopsis = "Párrafo 1.\nPárrafo 2.\nPárrafo 3."

        self._common.generateEbook()

        self.assertEqual(self._common.outputEpub.getDescription(), "Párrafo 1. Párrafo 2. Párrafo 3.")

    def test_tags_are_stripped_from_synopsis(self):
        self._common.metadata.synopsis = "Párrafo 1.\n<strong>Párrafo <em>2</em></strong>.\n<span>Párrafo 3.</span>"

        self._common.generateEbook()

        self.assertEqual(self._common.outputEpub.getDescription(), "Párrafo 1. Párrafo 2. Párrafo 3.")

    def test_simple_collection(self):
        self._common.metadata.subCollectionName = "Esta es la saga"
        self._common.metadata.collectionVolume = "9"

        self._common.generateEbook()

        calibreSerie = self._common.outputEpub.getCalibreSerie()
        self.assertEqual(calibreSerie, ("Esta es la saga", "9"))

    def test_sub_collections(self):
        self._common.metadata.collectionName = "Esta es la serie"
        self._common.metadata.subCollectionName = "Esta es la saga"
        self._common.metadata.collectionVolume = "9"

        self._common.generateEbook()

        calibreSerie = self._common.outputEpub.getCalibreSerie()
        self.assertEqual(calibreSerie, ("Esta es la serie: Esta es la saga", "9"))

    def test_strip_zeros_from_collection_volume_for_calibre_metadata(self):
        self._common.metadata.subCollectionName = "Esta es la saga"
        self._common.metadata.collectionVolume = "007"

        self._common.generateEbook()

        calibreSerie = self._common.outputEpub.getCalibreSerie()
        self.assertEqual(calibreSerie, ("Esta es la saga", "7"))

    def test_default_language(self):
        self._common.metadata.language = ""

        self._common.generateEbook()

        self.assertTrue(self._common.outputEpub.getLanguage(), "es")

    def test_language(self):
        self._common.metadata.language = "en"

        self._common.generateEbook()

        self.assertTrue(self._common.outputEpub.getLanguage(), "en")

    def test_default_genre(self):
        self._common.metadata.genres.clear()

        self._common.generateEbook()

        self.assertEqual(self._common.outputEpub.getSubject(), "Género, Subgéneros")

    def test_one_genretype_one_genre_one_subgenre(self):
        self._common.metadata.genres.append(ebook_metadata.Genre("Tipo1", "Genero1", "Subgenero1"))

        self._common.generateEbook()

        self.assertEqual(self._common.outputEpub.getSubject(), "Genero1, Subgenero1")

    def test_one_genretype_one_genre_two_subgenres(self):
        self._common.metadata.genres.append(ebook_metadata.Genre("Tipo1", "Genero1", "Subgenero1"))
        self._common.metadata.genres.append(ebook_metadata.Genre("Tipo1", "Genero1", "Subgenero2"))

        self._common.generateEbook()

        self.assertEqual(self._common.outputEpub.getSubject(), "Genero1, Subgenero1, Subgenero2")

    def test_one_genretype_two_genres_one_subgenre(self):
        self._common.metadata.genres.append(ebook_metadata.Genre("Tipo1", "Genero1", "Subgenero1"))
        self._common.metadata.genres.append(ebook_metadata.Genre("Tipo1", "Genero2", "Subgenero1"))

        self._common.generateEbook()

        self.assertEqual(self._common.outputEpub.getSubject(), "Genero1, Subgenero1, Genero2, Subgenero1")

    def test_one_genretype_two_genres_two_subgenres(self):
        self._common.metadata.genres.append(ebook_metadata.Genre("Tipo1", "Genero1", "Subgenero1"))
        self._common.metadata.genres.append(ebook_metadata.Genre("Tipo1", "Genero1", "Subgenero2"))
        self._common.metadata.genres.append(ebook_metadata.Genre("Tipo1", "Genero2", "Subgenero1"))
        self._common.metadata.genres.append(ebook_metadata.Genre("Tipo1", "Genero2", "Subgenero2"))

        self._common.generateEbook()

        self.assertEqual(self._common.outputEpub.getSubject(), "Genero1, Subgenero1, Subgenero2, Genero2, Subgenero1, Subgenero2")

    def test_genretype_not_get_saved(self):
        self._common.metadata.genres.append(ebook_metadata.Genre("Tipo1", "Genero1", "Subgenero1"))
        self._common.metadata.genres.append(ebook_metadata.Genre("Tipo1", "Genero1", "Subgenero2"))
        self._common.metadata.genres.append(ebook_metadata.Genre("Tipo2", "Genero2", "Subgenero1"))
        self._common.metadata.genres.append(ebook_metadata.Genre("Tipo2", "Genero2", "Subgenero2"))

        self._common.generateEbook()

        self.assertEqual(self._common.outputEpub.getSubject(), "Genero1, Subgenero1, Subgenero2, Genero2, Subgenero1, Subgenero2")

    def test_genres_are_sorted(self):
        self._common.metadata.genres.append(ebook_metadata.Genre("Tipo1", "d", "f"))
        self._common.metadata.genres.append(ebook_metadata.Genre("Tipo1", "k", "a"))
        self._common.metadata.genres.append(ebook_metadata.Genre("Tipo1", "a", "b"))
        self._common.metadata.genres.append(ebook_metadata.Genre("Tipo1", "u", "a"))
        self._common.metadata.genres.append(ebook_metadata.Genre("Tipo1", "a", "a"))
        self._common.metadata.genres.append(ebook_metadata.Genre("Tipo1", "d", "e"))

        self._common.generateEbook()

        self.assertEqual(self._common.outputEpub.getSubject(), "a, a, b, d, e, f, k, a, u, a")

    def test_default_publisher(self):
        self._common.generateEbook()

        self.assertEqual(self._common.outputEpub.getPublisher(), "ePubLibre")


class TocTest(unittest.TestCase):
    def setUp(self):
        self._common = Common()

    def tearDown(self):
        self._common.release()

    def test_author_entry_when_no_authors_and_include_optional_files(self):
        self._common.metadata.authors.clear()

        self._common.generateEbook()

        titles = self._common.outputEpub.getTitles()

        self.assertEqual(titles[-1], ("Autor", "autor.xhtml", []))

    def test_author_entry_when_male_author(self):
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla"))

        self._common.generateEbook()

        titles = [t[0] for t in self._common.outputEpub.getTitles()]

        self.assertEqual(titles[-1], "Autor")

    def test_author_entry_when_female_author(self):
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla", ebook_metadata.Person.FEMALE_GENDER))

        self._common.generateEbook()

        titles = [t[0] for t in self._common.outputEpub.getTitles()]

        self.assertEqual(titles[-1], "Autora")

    def test_author_entry_when_two_authors(self):
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla", ebook_metadata.Person.MALE_GENDER))
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla", ebook_metadata.Person.FEMALE_GENDER))

        self._common.generateEbook()

        titles = [t[0] for t in self._common.outputEpub.getTitles()]

        self.assertEqual(titles[-1], "Autores")

    def test_required_entries_when_not_include_optional_files(self):
        self._common.generateEbook(includeOptionalFiles=False)

        titles = self._common.outputEpub.getTitles()

        self.assertEqual(titles, [("Cubierta", "cubierta.xhtml", []), ("Título", "titulo.xhtml", [])])

    def test_notes_entry_exists_when_epub_contains_notes(self):
        ebookData = ebook_data.EbookData()
        ebookData.createNotesSection().save()

        self._common.generateEbook(ebookData)

        titles = self._common.outputEpub.getTitles()

        self.assertEqual(titles[-1], ("Notas", "notas.xhtml", []))

    def test_title_entry(self):
        self._common.metadata.title = "El título del libro"

        self._common.generateEbook()

        titles = [t[0] for t in self._common.outputEpub.getTitles()]

        self.assertEqual(titles[1], "El título del libro")

    def test_simple_toc(self):
        ebookData = ebook_data.EbookData()
        section = ebookData.createTextSection()

        for i in (1, 1, 2, 3, 1, 2):
            section.openHeading(i)
            section.appendText(str(i))
            section.closeHeading(i)

        section.save()

        self._common.generateEbook(ebookData, includeOptionalFiles=False)

        # Salteo los títulos de cubierta.xhtml y titulo.xhtml.
        titles = self._common.outputEpub.getTitles()[2:]
        self.assertEqual(titles,
                         [("1", "Section0001.xhtml#heading_id_1", []),
                          ("1", "Section0001.xhtml#heading_id_2", [
                              ("2", "Section0001.xhtml#heading_id_3", [
                                  ("3", "Section0001.xhtml#heading_id_4", [])])]),
                          ("1", "Section0001.xhtml#heading_id_5", [
                              ("2", "Section0001.xhtml#heading_id_6", [])])])

    def test_complex_toc(self):
        ebookData = ebook_data.EbookData()
        section = ebookData.createTextSection()

        for i in (1, 2, 3, 4, "N", 2, 2, 3, "N", 4, 1, "N", 2, 2, 3, 2, 3, 4, 5, "N", 6, 5, 5, 4, "N", 3, "N", 3, 4, 5, 3):
            if i == "N":
                section.save()
                section = ebookData.createTextSection()
            else:
                section.openHeading(i)
                section.appendText(str(i))
                section.closeHeading(i)

        section.save()

        self._common.generateEbook(ebookData, includeOptionalFiles=False)

        # Salteo título de cubierta.xhtml y titulo.xhtml.
        titles = self._common.outputEpub.getTitles()[2:]
        self.assertEqual(titles,
                         [("1", "Section0001.xhtml#heading_id_1", [
                             ("2", "Section0001.xhtml#heading_id_2", [
                                 ("3", "Section0001.xhtml#heading_id_3", [
                                     ("4", "Section0001.xhtml#heading_id_4", [])
                                 ])
                             ]),
                             ("2", "Section0002.xhtml#heading_id_5", []),
                             ("2", "Section0002.xhtml#heading_id_6", [
                                 ("3", "Section0002.xhtml#heading_id_7", [
                                     ("4", "Section0003.xhtml#heading_id_8", [])
                                 ])
                             ])]),
                          ("1", "Section0003.xhtml#heading_id_9", [
                              ("2", "Section0004.xhtml#heading_id_10", []),
                              ("2", "Section0004.xhtml#heading_id_11", [
                                  ("3", "Section0004.xhtml#heading_id_12", [])
                              ]),
                              ("2", "Section0004.xhtml#heading_id_13", [
                                  ("3", "Section0004.xhtml#heading_id_14", [
                                      ("4", "Section0004.xhtml#heading_id_15", [
                                          ("5", "Section0004.xhtml#heading_id_16", [
                                              ("6", "Section0005.xhtml#heading_id_17", [])
                                          ]),
                                          ("5", "Section0005.xhtml#heading_id_18", []),
                                          ("5", "Section0005.xhtml#heading_id_19", [])
                                      ]),
                                      ("4", "Section0005.xhtml#heading_id_20", [])
                                  ]),
                                  ("3", "Section0006.xhtml#heading_id_21", []),
                                  ("3", "Section0007.xhtml#heading_id_22", [
                                      ("4", "Section0007.xhtml#heading_id_23", [
                                          ("5", "Section0007.xhtml#heading_id_24", [])
                                      ])
                                  ]),
                                  ("3", "Section0007.xhtml#heading_id_25", [])
                              ])
                          ])])

    def test_strip_tags_from_title_text(self):
        ebookData = ebook_data.EbookData()
        section = ebookData.createTextSection()

        section.openHeading(1)
        section.openTag("em")
        section.appendText("Este es el título 1")
        section.closeTag("em")
        section.closeHeading(1)

        section.openHeading(1)
        section.appendText("Este es el ")
        section.openTag("em")
        section.appendText("título ")
        section.closeTag("em")
        section.openTag("strong")
        section.appendText("2")
        section.closeTag("strong")
        section.closeHeading(1)

        section.openHeading(1)
        section.appendText("Este ")
        section.openTag("span")
        section.appendText("es ")
        section.openTag("em")
        section.appendText("el título ")
        section.closeTag("em")
        section.openTag("strong")
        section.appendText("3")
        section.closeTag("strong")
        section.closeTag("span")
        section.closeHeading(1)

        section.openHeading(1)
        section.appendText("Título sin tags")
        section.closeHeading(1)

        section.save()

        self._common.generateEbook(ebookData, includeOptionalFiles=False)

        # Salteo los títulos de cubierta.xhtml y titulo.xhtml.
        titles = [t[0] for t in self._common.outputEpub.getTitles()[2:]]
        self.assertEqual(titles, ["Este es el título 1", "Este es el título 2", "Este es el título 3", "Título sin tags"])

    def test_replace_br_with_space(self):
        ebookData = ebook_data.EbookData()
        section = ebookData.createTextSection()

        section.openHeading(1)
        section.appendText("Título con un")
        section.openTag("br")
        section.closeTag("br")
        section.appendText("salto de línea manual")
        section.closeHeading(1)

        section.openHeading(1)
        section.appendText("Título con")
        section.openTag("strong")
        section.openTag("br")
        section.closeTag("br")
        section.appendText("dos saltos de")
        section.closeTag("strong")
        section.openTag("br")
        section.closeTag("br")
        section.appendText("líneas manuales")
        section.closeHeading(1)
        section.save()

        self._common.generateEbook(ebookData, includeOptionalFiles=False)

        # Salteo los títulos de cubierta.xhtml y titulo.xhtml.
        titles = [t[0] for t in self._common.outputEpub.getTitles()[2:]]
        self.assertEqual(titles, ["Título con un salto de línea manual", "Título con dos saltos de líneas manuales"])


class EpubFileNameTest(unittest.TestCase):
    def setUp(self):
        self._common = Common()

    def tearDown(self):
        self._common.release()

    def test_default_metadata(self):
        fileName = self._common.generateEbook()

        self.assertEqual(fileName, "Autor - Titulo [0000] (r1.0 Editor).epub")

    def test_one_author_and_no_collection(self):
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "Borges, Jorge Luis"))

        fileName = self._common.generateEbook()

        self.assertEqual(fileName, "Borges, Jorge Luis - Titulo [0000] (r1.0 Editor).epub")

    def test_two_authors_and_no_collection(self):
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "Borges, Jorge Luis"))
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "Shakespeare, William"))

        fileName = self._common.generateEbook()

        self.assertEqual(fileName, "Borges, Jorge Luis & Shakespeare, William - Titulo [0000] (r1.0 Editor).epub")

    def test_three_authors_and_no_collection(self):
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla"))
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla"))
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla"))

        fileName = self._common.generateEbook()

        self.assertEqual(fileName, "AA. VV. - Titulo [0000] (r1.0 Editor).epub")

    def test_one_author_and_simple_collection(self):
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "Borges, Jorge Luis"))
        self._common.metadata.subCollectionName = "Esta es la serie"
        self._common.metadata.collectionVolume = "10"

        fileName = self._common.generateEbook()

        self.assertEqual(fileName, "Borges, Jorge Luis - [Esta es la serie 10] Titulo [0000] (r1.0 Editor).epub")

    def test_one_author_and_subcollection(self):
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "Borges, Jorge Luis"))
        self._common.metadata.collectionName = "Esta es la saga"
        self._common.metadata.subCollectionName = "Esta es la serie"
        self._common.metadata.collectionVolume = "10"

        fileName = self._common.generateEbook()

        self.assertEqual(fileName, "[Esta es la saga] [Esta es la serie 10] Borges, Jorge Luis - Titulo [0000] (r1.0 Editor).epub")

    def test_two_authors_and_subcollection(self):
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "Borges, Jorge Luis"))
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "Shakespeare, William"))
        self._common.metadata.collectionName = "Esta es la saga"
        self._common.metadata.subCollectionName = "Esta es la serie"
        self._common.metadata.collectionVolume = "10"

        fileName = self._common.generateEbook()

        self.assertEqual(fileName, "[Esta es la saga] [Esta es la serie 10] Borges, Jorge Luis & "
                                   "Shakespeare, William - Titulo [0000] (r1.0 Editor).epub")

    def test_three_authors_and_subcollection(self):
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla"))
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla"))
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla"))
        self._common.metadata.collectionName = "Esta es la saga"
        self._common.metadata.subCollectionName = "Esta es la serie"
        self._common.metadata.collectionVolume = "10"

        fileName = self._common.generateEbook()

        self.assertEqual(fileName, "[Esta es la saga] [Esta es la serie 10] AA. VV. - Titulo [0000] (r1.0 Editor).epub")

    def test_bookid(self):
        self._common.metadata.authors.append(ebook_metadata.Person("Autor", "Autor"))
        self._common.metadata.bookId = "1234"

        fileName = self._common.generateEbook()

        self.assertEqual(fileName, "Autor - Titulo [1234] (r1.0 Editor).epub")

    def test_title(self):
        self._common.metadata.title = "Este es el título"

        fileName = self._common.generateEbook()

        self.assertEqual(fileName, "Autor - Este es el titulo [0000] (r1.0 Editor).epub")

    def test_editor(self):
        self._common.metadata.editor = "Este es el editor"

        fileName = self._common.generateEbook()

        self.assertEqual(fileName, "Autor - Titulo [0000] (r1.0 Este es el editor).epub")

    def test_special_characters(self):
        self._common.metadata.title = "Títúló dél libro"
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "Éste es el áutór"))
        self._common.metadata.editor = "Esté es él edítór"
        self._common.metadata.collectionName = "Esta es la ságá"
        self._common.metadata.subCollectionName = "Éstá es la série"
        self._common.metadata.collectionVolume = "10"

        fileName = self._common.generateEbook()

        self.assertEqual(fileName, "[Esta es la saga] [Esta es la serie 10] Este es el autor - "
                                   "Titulo del libro [0000] (r1.0 Este es el editor).epub")


class ImagesTest(unittest.TestCase):
    def setUp(self):
        self._common = Common()

    def tearDown(self):
        self._common.release()

    def test_required_images_exist(self):
        self._common.generateEbook()

        self.assertTrue(self._common.outputEpub.hasFile("cover.jpg"))
        self.assertTrue(self._common.outputEpub.hasFile("EPL_logo.png"))
        self.assertTrue(self._common.outputEpub.hasFile("ex_libris.png"))

    def test_cover_image_content(self):
        image = Image.new("RGB", (600, 900))
        buffer = io.BytesIO()
        image.save(buffer, "JPEG")

        self._common.metadata.coverImage = images.CoverImage(buffer.getvalue(), allowProcessing=False)

        self._common.generateEbook()

        coverImage = self._common.outputEpub.read(self._common.outputEpub.getFullPathToFile("cover.jpg"))
        self.assertEqual(coverImage, buffer.getvalue())

    def test_only_one_author_image_exists_when_no_authors_but_include_optional_files(self):
        self._common.metadata.authors.clear()

        self._common.generateEbook()

        authorImages = [f for f in self._common.outputEpub.getNamelist() if f.startswith("autor") and f.endswith(".jpg")]
        self.assertEqual(len(authorImages), 1)
        self.assertEqual(authorImages[0], "autor.jpg")

    def test_only_one_author_image_exists_when_one_author(self):
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla"))

        self._common.generateEbook()

        authorImages = [f for f in self._common.outputEpub.getNamelist() if f.startswith("autor") and f.endswith(".jpg")]
        self.assertEqual(len(authorImages), 1)
        self.assertEqual(authorImages[0], "autor.jpg")

    def test_two_author_images_exist_when_two_authors(self):
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla"))
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla"))

        self._common.generateEbook()

        authorImages = [f for f in self._common.outputEpub.getNamelist() if f.startswith("autor") and f.endswith(".jpg")]

        self.assertEqual(len(authorImages), 2)
        self.assertTrue("autor.jpg" in authorImages and "autor1.jpg" in authorImages)

    def test_two_author_images_exist_when_two_authors_and_both_have_biography_or_image(self):
        image = Image.new("RGB", (320, 400))
        buffer = io.BytesIO()
        image.save(buffer, "JPEG")

        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla", biography="bla"))
        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla", image=images.AuthorImage(buffer.getvalue(), allowProcessing=False)))

        self._common.generateEbook()

        authorImages = [f for f in self._common.outputEpub.getNamelist() if f.startswith("autor") and f.endswith(".jpg")]
        self.assertEqual(len(authorImages), 2)
        self.assertTrue("autor.jpg" in authorImages and "autor1.jpg" in authorImages)

    def test_author_image_content(self):
        image = Image.new("RGB", (320, 400))
        buffer = io.BytesIO()
        image.save(buffer, "JPEG")

        self._common.metadata.authors.append(ebook_metadata.Person("bla", "bla", image=images.AuthorImage(buffer.getvalue(), allowProcessing=False)))

        self._common.generateEbook()

        authorImage = self._common.outputEpub.read(self._common.outputEpub.getFullPathToFile("autor.jpg"))
        self.assertEqual(authorImage, buffer.getvalue())

    def test_author_image_content_when_author_has_custom_biography(self):
        image = Image.new("RGB", (320, 400))
        buffer = io.BytesIO()
        image.save(buffer, "JPEG")

        self._common.metadata.authors.append(ebook_metadata.Person("bla",
                                                                   "bla",
                                                                   biography="bla",
                                                                   image=images.AuthorImage(buffer.getvalue(), allowProcessing=False)))

        self._common.generateEbook()

        authorImage = self._common.outputEpub.read(self._common.outputEpub.getFullPathToFile("autor.jpg"))
        self.assertEqual(authorImage, buffer.getvalue())


class MiscTest(unittest.TestCase):
    def setUp(self):
        self._common = Common()

    def tearDown(self):
        self._common.release()

    def test_css_file_exists(self):
        self._common.generateEbook()

        self.assertTrue(self._common.outputEpub.hasFile("style.css"))

    def test_ibooks_display_options_file_exists(self):
        self._common.generateEbook()

        self.assertTrue(self._common.outputEpub.hasFile("com.apple.ibooks.display-options.xml"))


class Common:
    NAMESPACES = {"x": "http://www.w3.org/1999/xhtml"}

    def __init__(self):
        self._outputFile = tempfile.TemporaryFile()

        self.metadata = ebook_metadata.Metadata()
        self.outputEpub = None

    def xpath(self, element, xpath):
        return element.xpath(xpath, namespaces=Common.NAMESPACES)

    def generateEbook(self, ebookData=None, includeOptionalFiles=True):
        ebookData = ebookData or ebook_data.EbookData()

        eebook = ebook.Ebook(ebookData, self.metadata, includeOptionalFiles=includeOptionalFiles)
        fileName = eebook.save(self._outputFile)
        self.outputEpub = epub.EpubReader(self._outputFile)

        return fileName

    def release(self):
        self._outputFile.close()

        if self.outputEpub:
            self.outputEpub.close()


if __name__ == "__main__":
    unittest.main()