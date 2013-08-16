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

from misc import utils


class File:

    FILE_TYPE = utils.Utilities.enum(TEXT=1, IMAGE=2)

    def __init__(self, name, fileType, content):
        """
        Crea un nuevo File.

        @param name: el nombre del archivo.
        @param fileType: un valor FILE_TYPE indicando el tipo de archivo.
        @param content: el contenido del archivo, en string o bytes.
        """
        self.name = name
        self.fileType = fileType
        self.content = content


class Title:
    
    def __init__(self, titleLocation, text):
        """
        Crea un nuevo Title.

        @param titleLocation: la ubicación del título (el nombre del archivo donde se encuentra).
                              Ej: Section0000.xhtml#titulo1.
        @param text: el texto del título.
        """
        self.titleLocation = titleLocation
        self.text = text
        self.childTitles = []
        
    def addTitle(self, sectionName, text):
        """
        Agrega un título que tiene como padre al título actual.

        @param sectionName: nombre del archivo donde se encuentra el título.
        @param text: el texto del título.
        """        
        childTitle = Title(sectionName, text)
        self.childTitles.append(childTitle)
        return childTitle


class Metadata:

    def __init__(self):
        self.title = ""
        self.subtitle = ""
        self.authorBiography = ""
        self.synopsis = ""
        self.editor = ""
        self.originalTitle = ""

        # Saga
        self.collectionName = ""
        # Serie
        self.subCollectionName = ""
        # Volumen
        self.collectionVolume = ""

        # Una lista de Person con los autores
        self.authors = []

        # Una lista de Person con los traductores
        self.translators = []

        # Una lista de Person con los ilustradores
        self.ilustrators = []

        # Un date con la fecha de publicación en el idioma original
        self.publicationDate = None

        # Una lista de Genre con los géneros
        self.genres = []

        self.publisher = ""
        self.coverDesignOrTweak = ""
        self.coverDesigner = ""
        self.language = ""
        self.dedication = ""
        self.coverImage = None
        self.authorImage = None


class Person:

    def __init__(self, name, fileAs):
        self.name = name
        self.fileAs = fileAs


class Genre:

    def __init__(self, genreType, genre, subGenre):
        self.genreType = genreType
        self.genre = genre
        self.subGenre = subGenre