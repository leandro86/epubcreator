import os

from epubcreator.converters.converter_base import AbstractConverter

# Necesito realizar estos imports para que se registren las subclases y
# AbstractConverter.__subclasses__() las retorne correctamente a todas.
# TODO: cargar las subclases de AbstractConverter dinámicamente.
from epubcreator.converters.docx import docx_converter


class ConverterFactory():
    _converters = {}

    @staticmethod
    def getConverter(inputFilePath, **options):
        if not ConverterFactory._converters:
            ConverterFactory._loadConverters()

        fileType = os.path.splitext(inputFilePath)[1][1:]
        if fileType not in ConverterFactory._converters:
            raise Exception("No existe un convertidor para un archivo '{0}'.".format(fileType))

        return ConverterFactory._converters[fileType](inputFilePath, **options)

    @staticmethod
    def getAllConverters():
        if not ConverterFactory._converters:
            ConverterFactory._loadConverters()

        return ConverterFactory._converters.values()

    @staticmethod
    def _loadConverters():
        converterPackages = AbstractConverter.__subclasses__()
        for converterPackage in converterPackages:
            ConverterFactory._converters[converterPackage.FILE_TYPE] = converterPackage