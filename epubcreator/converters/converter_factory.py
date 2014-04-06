import os

from epubcreator.converters import converter_base


class ConverterFactory():
    _converters = {}

    @staticmethod
    def getConverter(inputFilePath, **options):
        if not ConverterFactory._converters:
            ConverterFactory._loadConverters()

        fileType = os.path.splitext(inputFilePath)[1][1:]
        if fileType not in ConverterFactory._converters:
            raise Exception("No existe un convertidor para un archivo {0}.".format(fileType))

        return ConverterFactory._converters[fileType](inputFilePath, **options)

    @staticmethod
    def _loadConverters():
        converters = converter_base.AbstractConverter.__subclasses__()
        for converter in converters:
            ConverterFactory._converters[converter.FILE_TYPE] = converter