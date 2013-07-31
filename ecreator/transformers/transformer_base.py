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


class AbstractTransformer:

    """
    Clase abstracta para obtener los archivos, títulos y metadatos de algún documento de origen.
    Cuando se quiera procesar algún tipo de documento nuevo, debe crearse una clase derivada de ésta y
    sobreescribir obligatoriamente el método "transform", y opcionalmente el método "getMetadata".
    """

    def __init__(self, inputFile):
        """
        """
        self._inputFile = inputFile

    def transform(self):
        """
        Obtiene los archivos y títulos de algún documento de origen.

        @return: un tupla de dos elementos que contiene: una lista de File y una lista de Title.
                 Por convención, la lista de File contiene primero las imágenes y demás archivos, y luego
                 vienen todos los htmls, en el orden en el cual deben ser insertados en el epub.
        """
        raise NotImplemented

    def getMetadata(self):
        """
        Obtiene los metadatos del documento de origen.

        @return: un objeto Metadata.
        """
        raise NotImplemented