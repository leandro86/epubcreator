from misc import utils


class AbstractConverter:
    def __init__(self, inputFile):
        self._inputFile = inputFile

    def convert(self):
        raise NotImplemented

    def getMetadata(self):
        raise NotImplemented


class ConverterLogMessage:
    MSG_TYPE = utils.Utilities.enum(WARNING=1, ERROR=2)

    def __init__(self, msgType, message):
        self.msgType = msgType
        self.message = message