class AbstractConverter:
    def __init__(self, inputFile):
        self._inputFile = inputFile

    def convert(self):
        raise NotImplemented

    def getMetadata(self):
        raise NotImplemented

    def getRawText(self):
        raise NotImplemented