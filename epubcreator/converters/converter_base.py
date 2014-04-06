import epubcreator.misc.options


class AbstractConverter(epubcreator.misc.options.Options):
    FILE_TYPE = ""

    def __init__(self, inputFilePath, **options):
        super().__init__(**options)

        self._inputFile = inputFilePath

    def convert(self):
        raise NotImplemented

    def getMetadata(self):
        raise NotImplemented

    def getRawText(self):
        raise NotImplemented