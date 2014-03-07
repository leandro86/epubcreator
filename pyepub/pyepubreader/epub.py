import zipfile
import os

from lxml import etree

from pyepub.pyepubreader import opf, toc


class EpubReader:
    """ Simple clase para leer el contenido de un epub, que la hice con el
        único de propósito de usarla para los unittests, por ahora. """

    def __init__(self, fileInput):
        """
        Abre un epub.

        @param fileInput: el path del epub a abrir, o un objeto de tipo file.
        """
        self._epub = zipfile.ZipFile(fileInput, "r")

        pathToOpf = self._getPathToOpf()
        # En el directorio donde esté ubicado content.opf, es donde se encuentran
        # el resto de los archivos
        self._rootDir = os.path.split(pathToOpf)[0]
        self._opf = opf.Opf(self._epub.read(pathToOpf))

        # No puedo hacer un os.path.join, porque imperiosamente necesito usar esta barra: "/" y
        # no esta "\".
        self._toc = toc.Toc(self._epub.read("/".join(("OEBPS", self._opf.getPathToToc()))))

    def getHtmlFileNamesReadingOrder(self):
        """
        Retorna los htmls en orden de lectura (según el playorder).

        @return: una lista de strings con el nombre de cada html.
        """
        return self._opf.getSpineItems()

    def hasFile(self, fileName):
        return any("/" + fileName in x for x in self._epub.namelist())

    def getAuthors(self):
        return self._opf.getAuthors()

    def getTranslators(self):
        return self._opf.getTranslators()

    def getIlustrators(self):
        return self._opf.getIlustrators()

    def getCalibreSerie(self):
        """
        Retorna la serie, especificada en el formato de calibre.

        @return: una tupla de strings: el primer elemento es el nombre de la serie, y el segundo el índice.
        """
        return self._opf.getCalibreSerie()

    def getTitles(self):
        return self._toc.getTitles()

    def read(self, fileName):
        """
        Lee el contenido de un archivo.

        @param fileName: el archivo a leer.

        @return: un string con el contenido.
        """
        return self._epub.read(fileName)

    def _getPathToOpf(self):
        container = etree.XML(self._epub.read("META-INF/container.xml"))
        return container.xpath("/inf:container/inf:rootfiles/inf:rootfile/@full-path",
                               namespaces={"inf": "urn:oasis:names:tc:opendocument:xmlns:container"})[0]

    def close(self):
        self._epub.close()