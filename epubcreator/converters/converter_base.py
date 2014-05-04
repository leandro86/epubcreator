import epubcreator.misc.options


class AbstractConverter(epubcreator.misc.options.Options):
    FILE_TYPE = ""

    def __init__(self, file, **options):
        super().__init__(**options)

        self._file = file

    def convert(self):
        raise NotImplemented

    def getMetadata(self):
        raise NotImplemented

    def getRawText(self):
        raise NotImplemented