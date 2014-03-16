class Genre:
    _FICTION_GENRES = (("Guión", "Obra compuesta o adaptada para medios masivos (cine, televisión, radio, Internet)."),
                       ("Novela", "Obra narrativa en prosa, extensa y compleja, de sucesos imaginados y \n"
                                  "parecidos a la realidad."),
                       ("Poesía", "Obra lírica, usualmente en verso, con fines estético-emocionales."),
                       ("Relato", "Obra narrativa en prosa, de menor extensión que la novela. \n"
                                  "Puede ser corta (Cuento) o mediana (Relato propiamente dicho)."),
                       ("Teatro", "Obra compuesta para ser representada en un escenario, ante público."))

    _FICTION_SUBGENRES = (("Aventuras", "Narra sucesos fuera de lo común, a menudo en escenarios exóticos. \n"
                                        "Incluye Acción, Exploradores, Piratas, Viajeros, Western."),
                          ("Bélico", "Trata de campañas, batallas o guerras. \n"
                                     "Suele presentar con detalle estrategias militares (reales o verosímiles)."),
                          ("Ciencia ficción", "Explora el impacto de posibles avances científicos, tecnológicos, \n"
                                              "sociales o culturales (presentes o futuros), sobre la sociedad \n"
                                              "o los individuos."),
                          ("Didáctico", "Con clara intención de dejar una enseñanza. Incluye Fábulas, Parábolas."),
                          ("Drama", "Narra hechos que conmueven al lector, usualmente desembocando en un final \n"
                                    "trágico. Incluye, por supuesto, Tragedia."),
                          ("Erótico", "Se relaciona directamente con la sensualidad y el sexo, presentándolos de \n"
                                      "forma implícita o explícita."),
                          ("Fantástico", "Utiliza la magia y otras formas sobrenaturales como un elemento primario \n"
                                         "del argumento, la temática o el ambiente. Incluye Mitología."),
                          ("Filosófico", "Una parte significativa de la obra se dedica a la filosofía discursiva (en \n"
                                         "temas como la función y el papel de la sociedad, el propósito de \n"
                                         "la vida, la ética o la moral, el papel del arte en la vida humana y el rol \n"
                                         "de la experiencia o la razón en el desarrollo del conocimiento). \n"
                                         "Incluye Novela de ideas."),
                          ("Histórico", "Ofrece una visión verosímil de una época histórica (preferiblemente lejana). "
                                        "\nSuele utilizar acontecimientos verídicos aunque los personajes "
                                        "principales \nsean inventados."),
                          ("Humor", "Usa el absurdo, en personajes o situaciones, para provocar la hilaridad. \n"
                                    "Incluye Comedia."),
                          ("Infantil", "Dirigido a los niños. Incluye Cuentos de hadas."),
                          ("Interactivo", "Exige una participación más activa del lector, que puede escoger \n"
                                          "varios «caminos» argumentales."),
                          ("Intriga", "Las acciones se ejecutan con inteligencia y astucia, y ocultan "
                                      "acontecimientos \nimportantes para suscitar interés y tensión en el lector. \n"
                                      "Incluye Misterio, Suspenso."),
                          ("Juvenil", "Dirigido a adolescentes y jóvenes."),
                          ("Policial", "Su móvil principal es la resolución de un enigma, generalmente \n"
                                       "criminal, mediante procesos mentales (como la deducción). \n"
                                       "Incluye Novela negra, Espionaje."),
                          ("Psicológico", "Enfatiza la caracterización interior de sus personajes, sus \n"
                                          "motivos, circunstancias y acción interna. Usa técnicas como flujo de \n"
                                          "conciencia o monólogo interior."),
                          ("Realista", "Apela a recursos pseudo documentales, principalmente para denunciar una \n"
                                       "situación injusta (social o individual). \n"
                                       "Incluye Costumbrismo, Narrativa social."),
                          ("Romántico", "Su tema primordial es el amor y las relaciones de pareja. (No se trata del \n"
                                        "movimiento Romanticismo de los siglos XVIII y XIX)."),
                          ("Sátira", "A diferencia del mero humor, apela a la ironía y el sarcasmo, con propósito \n"
                                     "moralizador, lúdico o meramente burlesco. Incluye Parodia, Picaresca."),
                          ("Terror", "Busca provocar el espanto en el lector, frecuentemente a través de elementos \n"
                                     "paranormales. Incluye Gore, Gótico, Horror, Thriller."),
                          ("Otros", "De no ubicarse en ninguno de los subgéneros anteriores."))

    _NON_FICTION_GENRES = (("Crónica", "Texto con estructura esencialmente cronológica, que suele emplear recursos \n"
                                       "literarios o periodísticos."),
                           ("Divulgación", "Texto informativo, sin excesivo rigor metodológico, que interpreta y "
                                           "hace \naccesible el conocimiento científico al público general."),
                           ("Ensayo", "Texto que presenta un punto de vista personal y subjetivo, sin aparato \n"
                                      "documental, de manera libre y asistemática y con voluntad de estilo."),
                           ("Referencia", "Texto con rigor académico/científico y estructura \n"
                                          "sistematizada, normalmente dividida en apartados o lecciones."))

    _NON_FICTION_SUBGENRES = (("Arte", "(Arquitectura, Danza, Escultura, Música, Pintura...)."),
                              ("Autoayuda", "(Superación)."),
                              ("Ciencias exactas", "(Lógica, Matemática...)."),
                              ("Ciencias naturales", "(Astronomía, Biología, Geología, Geografía, Física, "
                                                     "Química...)."),
                              ("Ciencias sociales", "(Administración, Antropología, Arqueología, Demografía, "
                                                    "Derecho, \nEconomía, Educación, Política, Sociología...). \n"
                                                    "Excepciones, por popularidad: Historia, Psicología."),
                              ("Comunicación", "(Cine, Diseño gráfico, Espectáculo, Fotografía, Historieta, \n"
                                               "Lingüística, Periodismo, Publicidad, Televisión...)."),
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
                              ("Otros", "De no ubicarse en ninguno de los subgéneros anteriores."))

    _TYPES = {"Ficción": [_FICTION_GENRES, _FICTION_SUBGENRES], "No Ficción": [_NON_FICTION_GENRES,
                                                                               _NON_FICTION_SUBGENRES]}

    @staticmethod
    def getTypes():
        return [genreType for genreType in Genre._TYPES.keys()]

    @staticmethod
    def getGenres(genreType):
        return Genre._TYPES[genreType][0]

    @staticmethod
    def getSubGenres(genreType):
        return Genre._TYPES[genreType][1]