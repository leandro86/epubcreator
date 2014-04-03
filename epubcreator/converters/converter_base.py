import epubcreator.misc.options


class AbstractConverter(epubcreator.misc.options.Options):
    def __init__(self, inputFile, **options):
        super().__init__(**options)

        self._inputFile = inputFile

    def convert(self):
        raise NotImplemented

    def getMetadata(self):
        raise NotImplemented

    def getRawText(self):
        raise NotImplemented