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
                          "seas, Señor, Padre que estás en lo alto! Todo esto me han urdido mis enemigos malvados».\n"
                          '<p class="salto05">A<small>NÓNIMO</small></p>')

    DEFAULT_AUTHOR_BIOGRAPHY = ("NOMBRE DEL AUTOR (Reikiavik, Islandia, 2013 - Terra III, 3096). Lorem ipsum dolor sit amet, consectetur "
                                "adipiscing elit. Nunc vel libero sed est ultrices elementum at vel lacus. Sed laoreet, velit nec congue "
                                "pellentesque, quam urna pretium nunc, et ultrices nulla lacus non libero.\n"
                                "Integer eu leo justo, vel sodales arcu. Donec posuere nunc in lectus laoreet a rhoncus enim fermentum. "
                                "Nunc luctus accumsan ligula eu molestie.")

    DEFAULT_COVER_MODIFICATION = "Diseño"

    # Las modificaciones posibles que pueden hacerse a la cubierta.
    COVER_MODIFICATION_OPTIONS = (("Diseño", "Elija esta opción si se conserva la cubierta original aun con algún ajuste menor de "
                                             "contraste y color (de la que, eso sí, es obligatorio quitar el logo o cualquier referencia "
                                             "a la editorial). Debe introducirse el nombre del diseñador de la cubierta. Si la cubierta es "
                                             "una creación original, debe introducirse el alias (o, si él quiere, el nombre) del creador."),
                                  ("Retoque", "Elija esta opción si la cubierta original se ha modificado significativamente. Deben "
                                              "introducirse los nombres del diseñador original y el alias de quien la haya retocado."))

    # Todos los géneros posibles.
    # Es un diccionario de la siguiente forma:
    # Key -> el tipo de género
    # Value -> una tupla de dos elementos:
    #           1 -> los géneros: un conjunto de tuplas de dos elementos:
    #                               1 -> el nombre del género.
    #                               2 -> la descripción del género.
    #           2 -> los subgéneros: un conjunto de tuplas de dos elementos:
    #                               1 -> el nombre del subgénero.
    #                               2 -> la descripción del subgénero.
    GENRES = {
        "Ficción": (
            (
                ("Guion", "Obra compuesta o adaptada para medios masivos (cine, televisión, radio, Internet)."),
                ("Novela", "Obra narrativa en prosa, extensa y compleja, de sucesos imaginados y parecidos a la realidad."),
                ("Poesía", "Obra lírica, usualmente en verso, con fines estético-emocionales."),
                ("Relato", "Obra narrativa en prosa, de menor extensión que la novela. Puede ser corta (Cuento) o mediana "
                           "(Relato propiamente dicho)."),
                ("Teatro", "Obra compuesta para ser representada en un escenario, ante público.")),
            (
                ("Aventuras", "Narra sucesos fuera de lo común, a menudo en escenarios exóticos. Incluye Acción, Exploradores, "
                              "Piratas, Viajeros, Western."),
                ("Bélico", "Trata de campañas, batallas o guerras. Suele presentar con detalle estrategias militares (reales o "
                           "verosímiles)."),
                ("Ciencia ficción", "Explora el impacto de posibles avances científicos, tecnológicos, sociales o culturales "
                                    "(presentes o futuros), sobre la sociedad o los individuos."),
                ("Didáctico", "Con clara intención de dejar una enseñanza. Incluye Fábulas, Parábolas."),
                ("Drama", "Narra hechos que conmueven al lector, usualmente desembocando en un final trágico. Incluye, por "
                          "supuesto, Tragedia."),
                ("Erótico", "Se relaciona directamente con la sensualidad y el sexo, presentándolos de forma implícita "
                            "o explícita."),
                ("Fantástico", "Utiliza la magia y otras formas sobrenaturales como un elemento primario del argumento, "
                               "la temática o el ambiente. Incluye Mitología."),
                ("Filosófico", "Una parte significativa de la obra se dedica a la filosofía discursiva (en temas como la "
                               "función y el papel de la sociedad, el propósito de la vida, la ética o la moral, el papel "
                               "del arte en la vida humana y el rol de la experiencia o la razón en el desarrollo del "
                               "conocimiento). Incluye Novela de ideas."),
                ("Histórico", "Ofrece una visión verosímil de una época histórica (preferiblemente lejana). Suele utilizar "
                              "acontecimientos verídicos aunque los personajes principales sean inventados."),
                ("Humor", "Usa el absurdo, en personajes o situaciones, para provocar la hilaridad. Incluye Comedia."),
                ("Infantil", "Dirigido a los niños. Incluye Cuentos de hadas."),
                ("Interactivo", "Exige una participación más activa del lector, que puede escoger varios «caminos» argumentales."),
                ("Intriga", "Las acciones se ejecutan con inteligencia y astucia, y ocultan acontecimientos importantes "
                            "para suscitar interés y tensión en el lector. Incluye Misterio, Suspenso."),
                ("Juvenil", "Dirigido a adolescentes y jóvenes."),
                ("Policial", "Su móvil principal es la resolución de un enigma, generalmente criminal, mediante procesos "
                             "mentales (como la deducción). Incluye Novela negra, Espionaje."),
                ("Psicológico", "Enfatiza la caracterización interior de sus personajes, sus motivos, circunstancias y "
                                "acción interna. Usa técnicas como flujo de conciencia o monólogo interior."),
                ("Realista", "Apela a recursos pseudo documentales, principalmente para denunciar una situación injusta (social "
                             "o individual). Incluye Costumbrismo, Narrativa social."),
                ("Romántico", "Su tema primordial es el amor y las relaciones de pareja. (No se trata del movimiento "
                              "Romanticismo de los siglos XVIII y XIX)."),
                ("Sátira", "A diferencia del mero humor, apela a la ironía y el sarcasmo, con propósito moralizador, lúdico o "
                           "meramente burlesco. Incluye Parodia, Picaresca."),
                ("Terror", "Busca provocar el espanto en el lector, frecuentemente a través de elementos paranormales. "
                           "Incluye Gore, Gótico, Horror, Thriller."),
                ("Otros", "De no ubicarse en ninguno de los subgéneros anteriores.")
            )
        ),
        "No Ficción": (
            (
                ("Crónica", "Texto con estructura esencialmente cronológica, que suele emplear recursos literarios o periodísticos."),
                ("Divulgación", "Texto informativo, sin excesivo rigor metodológico, que interpreta y hace accesible el conocimiento "
                                "científico al público general."),
                ("Ensayo", "Texto que presenta un punto de vista personal y subjetivo, sin aparato documental, de manera libre y asistemática "
                           "y con voluntad de estilo."),
                ("Referencia", "Texto con rigor académico/científico y estructura sistematizada, normalmente dividida en apartados "
                               "o lecciones.")),
            (
                ("Arte", "(Arquitectura, Danza, Escultura, Música, Pintura...)."),
                ("Autoayuda", "(Superación)."),
                ("Ciencias exactas", "(Lógica, Matemática...)."),
                ("Ciencias naturales", "(Astronomía, Biología, Geología, Geografía, Física, Química...)."),
                ("Ciencias sociales", "(Administración, Antropología, Arqueología, Demografía, Derecho, Economía, Educación, Política, "
                                      "Sociología...). Excepciones, por popularidad: Historia, Psicología."),
                ("Comunicación", "(Cine, Diseño gráfico, Espectáculo, Fotografía, Historieta, Lingüística, Periodismo, Publicidad, "
                                 "Televisión...)."),
                ("Crítica y teoría literaria", ""),
                ("Deportes y juegos", ""),
                ("Diccionarios y enciclopedias", ""),
                ("Espiritualidad", "(Esoterismo, Religión)."),
                ("Filosofía", ""),
                ("Historia", ""),
                ("Hogar", "(Bricolaje, Cocina, Decoración, Jardinería, Mascotas...)."),
                ("Humor", ""),
                ("Idiomas", ""),
                ("Manuales y cursos", ""),
                ("Memorias", "(Autobiografía, Biografía, Cartas, Diarios...)."),
                ("Padres e hijos", ""),
                ("Psicología", "(Psiquiatría...). Excepciones: Autoayuda, Sexualidad, Padres e hijos."),
                ("Salud y bienestar", "(Medicina, Nutrición, Terapias alternativas...)."),
                ("Sexualidad", ""),
                ("Tecnología", "(Electrónica, Industria, Informática, Telecomunicaciones...)."),
                ("Viajes", ""),
                ("Otros", "De no ubicarse en ninguno de los subgéneros anteriores.")
            )
        )}

    def __init__(self):
        self._publicationDate = None

        self.title = ""
        self.synopsis = ""
        self.bookId = ""

        self.subtitle = ""
        self.editor = ""
        self.originalTitle = ""

        # Saga.
        self.collectionName = ""
        # Serie.
        self.subCollectionName = ""
        # Volumen.
        self.collectionVolume = ""

        # Una lista de Person con los autores.
        self.authors = []

        # Una lista de Person con los traductores.
        self.translators = []

        # Una lista de Person con los ilustradores.
        self.ilustrators = []

        # Una lista de Genre con los géneros.
        self.genres = []

        self.coverModification = ""
        self.coverDesigner = ""
        self.language = ""
        self.dedication = ""
        self.coverImage = None

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


class Person:
    MALE_GENDER = 0
    FEMALE_GENDER = 1

    def __init__(self, name, fileAs, gender=MALE_GENDER, image=None, biography=None):
        self.name = name
        self.fileAs = fileAs
        self.gender = gender
        self.image = image
        self.biography = biography


class Genre:
    def __init__(self, genreType, genre, subGenre):
        self.genreType = genreType
        self.genre = genre
        self.subGenre = subGenre