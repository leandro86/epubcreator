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