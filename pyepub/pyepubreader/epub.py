import zipfile

from lxml import etree

from pyepub.pyepubreader import opf_reader


class EpubReader:
    def __init__(self, fileInput):
        """
        Abre un epub.

        @param fileInput: el path del epub a abrir, o un objeto de tipo file.
        """
        self._epub = zipfile.ZipFile(fileInput, "r")
        self._opfReader = opf_reader.OpfReader(self._epub.read(self._getPathToOpf()))

    def getHtmlFileNamesReadingOrder(self):
        """
        Retorna los htmls en orden de lectura (según el playorder).

        @return: una lista de strings con el nombre de cada html.
        """
        return self._opfReader.getSpineItems()

    def getAuthors(self):
        return self._opfReader.getAuthors()

    def getTranslators(self):
        return self._opfReader.getTranslators()

    def getIlustrators(self):
        return self._opfReader.getIlustrators()

    def getCalibreSerie(self):
        """
        Retorna la serie, especificada en el formato de calibre.

        @return: una tupla de strings: el primer elemento es el nombre de la serie, y el segundo el índice.
        """
        return self._opfReader.getCalibreSerie()

    def read(self, fileName):
        """
        Lee el contenido de un archivo.

        @param fileName: el archivo a leer.

        @return: un string con el contenido.

        @raise: KeyError: si no se encuentra el archivo.
        """
        return self._epub.read(fileName)

    def _getPathToOpf(self):
        container = etree.XML(self._epub.read("META-INF/container.xml"))
        return container.xpath("/inf:container/inf:rootfiles/inf:rootfile/@full-path",
                               namespaces={"inf": "urn:oasis:names:tc:opendocument:xmlns:container"})[0]

    def close(self):
        self._epub.close()