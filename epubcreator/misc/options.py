import types


class Options:
    """
    Brinda un mecanismo simple para aquellas clases que requieren que se provean diversas
    opciones para realizar su función.

    Lo único que se debe hacer es:

    1- Crear una clase descendiente de Options.
    2- Asignarle a la variable estática OPTIONS una lista de OPTION, con todas las posibles
       opciones que la clase admite.
    3- A cada opción se accede a través del objeto _options, que contiene un atributo con el
       nombre de la opción por cada una de las opciones especificadas en OPTIONS.
    4- El consumer especifica las opciones a modificar a través del método setOptions.
    """

    OPTIONS = []

    def __init__(self):
        self._options = types.SimpleNamespace()

        for option in type(self).OPTIONS:
            setattr(self._options, option.name, option.value)

    @classmethod
    def getOptionDescription(cls, optionName):
        return next((option.description for option in cls.OPTIONS if option.name == optionName))

    def setOptions(self, **options):
        for name, value in options.items():
            setattr(self._options, name, value)


class Option():
    def __init__(self, name, value, choices=None, description=None):
        self.name = name
        self.value = value
        self.choices = choices
        self.description = description