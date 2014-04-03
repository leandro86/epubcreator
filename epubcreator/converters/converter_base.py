from epubcreator.misc import options


class AbstractConverter(options.Options):
    def __init__(self, inputFile):
        super().__init__()

        self._inputFile = inputFile

    def convert(self):
        raise NotImplemented

    def getMetadata(self):
        raise NotImplemented

    def getRawText(self):
        raise NotImplemented