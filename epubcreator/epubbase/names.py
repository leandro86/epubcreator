import os

from epubcreator import config

COVER_FILENAME = "cubierta.xhtml"
SYNOPSIS_FILENAME = "sinopsis.xhtml"
TITLE_FILENAME = "titulo.xhtml"
INFO_FILENAME = "info.xhtml"
DEDICATION_FILENAME = "dedicatoria.xhtml"
AUTHOR_FILENAME = "autor.xhtml"
NOTES_FILENAME = "notas.xhtml"
COVER_IMAGE_FILENAME = "cover.jpg"
AUTHOR_IMAGE_FILENAME = "autor.jpg"
EPL_LOGO_FILENAME = "EPL_logo.png"
EX_LIBRIS_FILENAME = "ex_libris.png"
STYLE_FILENAME = "style.css"
IBOOKS_DISPLAY_OPTIONS_FILE_NAME = "com.apple.ibooks.display-options.xml"


def generateTextSectionName(sectionNumber):
    return "Section{0:04}.xhtml".format(sectionNumber)


def generateAuthorImageFileName(imageNumber):
    return AUTHOR_IMAGE_FILENAME if imageNumber == 0 else AUTHOR_IMAGE_FILENAME[:-4] + str(imageNumber) + AUTHOR_IMAGE_FILENAME[-4:]


def generateAuthorFileName(authorNumber):
    return AUTHOR_FILENAME if authorNumber == 0 else AUTHOR_FILENAME[:-6] + str(authorNumber) + AUTHOR_FILENAME[-6:]


def getFullPathToFile(file):
    """
    Retorna el path completo hacia el archivo del epubbase pasado como parámetro.

    @param file: una de las posibles constantes definidas en este archivo, por
                 ejemplo: COVER_FILENAME, TITLE_FILENAME, etc.
    """
    return os.path.join(config.EPUBBASE_FILES_DIR_PATH, file)