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

import zipfile
import io

from lxml import etree

from ecreator.transformers import transformer_base
from ecreator import ebook_data, fi
import config


class DocxTransformer(transformer_base.AbstractTransformer):

    def __init__(self, inputFile, ignoreEmptyParagraphs = True):
        super().__init__(inputFile)

        self._params = locals()

        # Nombré los parámetros del método de igual manera a como están en la planilla de transformación.
        # Solo me interesan los argumentos para la planilla. Borro todoo el resto de variables locales.
        del(self._params["self"])
        del(self._params["__class__"])
        del(self._params["inputFile"])
        self._prepareParams(self._params)

    def transform(self):
        document, footnotes, styles, documentRels, images = self._openDocx()

        parser = etree.XMLParser()
        parser.resolvers.add(_DocxResolver(footnotes, styles, documentRels))

        docxXslt = etree.parse(config.DOCX_TO_EPUB_STYLESHEET_PATH, parser)
        transformer = etree.XSLT(docxXslt)

        ffi = fi.Fi(str(transformer(document, **self._params)))
        files, titles = ffi.parse()

        # Agrego las imágenes al principio de la lista de archivos
        for imageName, imageData in images:
            files.insert(0, ebook_data.File(imageName, ebook_data.File.FILE_TYPE.IMAGE, imageData))

        # Parseo la lista de warnings y errores de la planilla, si los hay
        logMessages = []
        for msg in [w.message.split("**DOCX_WARNING**")[1] for w in transformer.error_log if
                    w.message.startswith("**DOCX_WARNING**")]:
            msgType = transformer_base.TransformerLogMessage.MSG_TYPE.WARNING
            logMessage = transformer_base.TransformerLogMessage(msgType, msg)
            logMessages.append(logMessage)

        return files, titles, logMessages

    def _openDocx(self):
        """
        Abre el docx y extrae los archivos necesarios para su procesamiento.

        @return: una tupla, cuyos elementos son:
                    1:  el documento donde se encuentra el texto, un objeto lxml ElementTree.
                    2:  el documento con las notas, en bytes.
                    3:  el documento con los estilos, en bytes.
                    4:  el documento con las relaciones, en bytes.
                    5:  las imágenes, un tupla cuyo primer elemento es el nombre de la
                        imagen, y el segundo el contenido de la misma en bytes.
        """
        with zipfile.ZipFile(self._inputFile) as docx:
            try:
                footnotes = docx.read("word/footnotes.xml")
            except KeyError:
                footnotes = None

            try:
                styles = docx.read("word/styles.xml")
            except KeyError:
                styles = None

            documentRels = docx.read("word/_rels/document.xml.rels")

            document = etree.parse(docx.open("word/document.xml"))

            imagesName = [imageName for imageName in docx.namelist() if imageName.startswith("word/media") and
                                                                        imageName.endswith(fi.Fi.VALID_IMAGE_TYPES)]
            images = [(image.split("/")[-1], docx.read(image)) for image in imagesName]

            return document, footnotes, styles, documentRels, images

    def _prepareParams(self, params):
        # Solamente puedo pasarle a la planilla strings como parámetros, por eso debo convertir los booleans.
        for key, value in list(params.items()):
            if isinstance(value, bool):
                value = "Y" if value else "N"
                params[key] = etree.XSLT.strparam(value)


class _DocxResolver(etree.Resolver):

    def __init__(self, footnotes, styles, documentRels):
        self._footnotes = footnotes
        self._styles = styles
        self._documentRels = documentRels

    def resolve(self, url, pubid, context):
        if "footnotes_path" in url.lower():
            if self._footnotes:
                return self.resolve_file(io.BytesIO(self._footnotes), context)
            else:
                return self.resolve_empty(context)
        elif "styles_path" in url.lower():
            if self._styles:
                return self.resolve_file(io.BytesIO(self._styles), context)
            else:
                self.resolve_empty(context)
        elif "rels_path" in url.lower():
            return self.resolve_file(io.BytesIO(self._documentRels), context)