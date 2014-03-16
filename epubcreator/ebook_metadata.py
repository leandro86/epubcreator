import datetime
import math


class Metadata:
    DEFAULT_TITLE = "Título"
    DEFAULT_AUTHOR = "Autor"
    DEFAULT_EDITOR = "Editor"
    DEFAULT_LANGUAGE = "es"
    DEFAULT_BOOK_ID = "0000"
    DEFAULT_SYNOPSIS = ("Yo por bien tengo que cosas tan señaladas, y por ventura nunca oídas ni vistas, vengan a noticia de muchos y no se "
                        "entierren en la sepultura del olvido, pues podría ser que alguno que las lea halle algo que le agrade, y a los que "
                        "no ahondaren tanto los deleite.\n"
                        "Y a este propósito dice Plinio que no hay libro, por malo que sea, que no tenga alguna cosa buena; mayormente que "
                        "los gustos no son todos unos, mas lo que uno no come, otro se pierde por ello. "
                        '<span class="nosep">L<small>ÁZARO</small></span> <small>DE</small> '
                        '<span class="nosep">T<small>ORMES</small>.</span>')

    # En el epubbase, en la dedicatoria de ejemplo, el segundo párrafo lleva la clase "salto05", por eso utilizo directamente el
    # tag "p" para poder agregar la clase, ya que de otra manera me sería imposible hacerlo.
    DEFAULT_DEDICATION = ("Suspiró entonces mío Cid, de pesadumbre cargado, y comenzó a hablar así, justamente mesurado: «¡Loado "
                          "seas, Señor, Padre que estás en lo alto! Todo esto me han urdido mis enemigos malvados»."
                          '<p class="salto05">A<small>NÓNIMO</small></p>')

    DEFAULT_AUTHOR_BIOGRAPHY = ("N<small>OMBRE DEL</small> A<small>UTOR</small> (Reikiavik, Islandia, 2013 - Terra III, 3096). Lorem "
                                "ipsum dolor sit amet, consectetur adipiscing elit. Nunc vel libero sed est ultrices elementum at vel "
                                "lacus. Sed laoreet, velit nec congue pellentesque, quam urna pretium nunc, et ultrices nulla lacus "
                                "non libero.\n"
                                "Integer eu leo justo, vel sodales arcu. Donec posuere nunc in lectus laoreet a rhoncus enim fermentum. "
                                "Nunc luctus accumsan ligula eu molestie.")

    DEFAULT_COVER_MODIFICATION = "Diseño"
    COVER_MODIFICATION_OPTIONS = (("Diseño", "Elija esta opción si se conserva la cubierta original aun con algún ajuste menor de "
                                             "contraste y color (de la que, eso sí, es obligatorio quitar el logo o cualquier referencia "
                                             "a la editorial). Debe introducirse el nombre del diseñador de la cubierta. \n"
                                             "Si la cubierta es una creación original, debe introducirse el alias (o, si él quiere, "
                                             "el nombre) del creador."),
                                  ("Retoque", "Elija esta opción si la cubierta original se ha modificado significativamente. Deben "
                                              "introducirse los nombres del diseñador original y el alias de quien la haya retocado."))

    def __init__(self):
        self._publicationDate = None

        self.title = ""
        self.synopsis = ""
        self.bookId = ""

        self.subtitle = ""
        self.authorBiography = ""
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

        # Una lista de Genre con los géneros
        self.genres = []

        self.coverModification = ""
        self.coverDesigner = ""
        self.language = ""
        self.dedication = ""
        self.coverImage = None
        self.authorImage = None

    # Un date con la fecha de publicación en el idioma original.
    @property
    def publicationDate(self):
        return self._publicationDate

    @publicationDate.setter
    def publicationDate(self, value):
        if type(value) is datetime.date or value is None:
            self._publicationDate = value
        else:
            raise ValueError("Date expected.")

    def getAuthorsAsText(self):
        return self._getPersonsListAsText(self.authors)

    def getIlustratorsAsText(self):
        return self._getPersonsListAsText(self.ilustrators)

    def getTranslatorsAsText(self):
        return self._getPersonsListAsText(self.translators)

    @staticmethod
    def convertNameToFileAsFormat(name):
        """
        Convierte un nombre al formato file-as.
        Ejemplo: "Edgar Allan Poe" es convertido en: "Poe, Edgar Allan".

        @param name: un string con el nombre a convertir.

        @return: un string con el nombre convertido.
        """
        words = name.split(" ")
        if len(words) > 1:
            pivot = math.ceil(len(words) / 2)
            orderedName = []

            words[-1] += ","

            for i in range(pivot, len(words)):
                orderedName.append(words[i])

            for i in range(pivot):
                orderedName.append(words[i])

            return " ".join(orderedName)
        else:
            return name

    def _getPersonsListAsText(self, persons):
        """
        Convierte una lista de Person a texto. Cada Person se concatena con un & (ampersand).

        @param persons: una lista de Person.

        @return: una tupla cuyo primer elemento es un string concatenado con todos los nombres, y el
                 segundo un string concatenado con todos los file-as.
        """
        return " & ".join((p.name for p in persons)), " & ".join((p.fileAs for p in persons))


class Person:
    def __init__(self, name, fileAs):
        self.name = name
        self.fileAs = fileAs


class Genre:
    def __init__(self, genreType, genre, subGenre):
        self.genreType = genreType
        self.genre = genre
        self.subGenre = subGenre