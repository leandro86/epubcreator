import types


class Options:
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