class Metadata:
    DEFAULT_TITLE = "Título"
    DEFAULT_AUTHOR = "Autor"
    DEFAULT_EDITOR = "Editor"
    DEFAULT_LANGUAGE = "es"
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

    def __init__(self):
        self.title = ""
        self.synopsis = ""

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

    def addAuthor(self, name, fileAs=None):
        self.authors.append(Person(name, fileAs or name))

    def addIlustrator(self, name, fileAs=None):
        self.ilustrators.append(Person(name, fileAs or name))

    def addTranslator(self, name, fileAs=None):
        self.translators.append(Person(name, fileAs or name))

    def addGenre(self, genreType, genre, subGenre):
        self.genres.append(Genre(genreType, genre, subGenre))


class Person:
    def __init__(self, name, fileAs):
        self.name = name
        self.fileAs = fileAs


class Genre:
    def __init__(self, genreType, genre, subGenre):
        self.genreType = genreType
        self.genre = genre
        self.subGenre = subGenre