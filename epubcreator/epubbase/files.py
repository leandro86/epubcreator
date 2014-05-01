import os

import mako.template

from epubcreator import config


class EpubBaseFiles:
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
    APPLE_XML = "com.apple.ibooks.display-options.xml"
    BLACK_LOGO_FOR_COVER = "black_logo_for_cover.png"
    WHITE_LOGO_FOR_COVER = "white_logo_for_cover.png"
    GLOW_LOGO_FOR_COVER = "glow_logo_for_cover.png"
    BLACK_LOGO_PREVIEW = "black_logo_preview.png"
    WHITE_LOGO_PREVIEW = "white_logo_preview.png"
    GLOW_LOGO_PREVIEW = "glow_logo_preview.png"

    # Archivos que son templates de mako.
    _TEMPLATES = (AUTHOR_FILENAME,
                  DEDICATION_FILENAME,
                  INFO_FILENAME,
                  SYNOPSIS_FILENAME,
                  TITLE_FILENAME)

    # Key: -> un nombre de archivo.
    # Value: -> el contenido del archivo en bytes si no es un template, sino el template de mako.
    # Los archivos se leen y se cargan según se vayan necesitando.
    _FILES = {}

    @staticmethod
    def getFile(file):
        """
        Retorna los bytes de un archivo del epubbase que no sea un template de mako. Para los templates de
        mako usar el método correspondiente.

        @param file: algunas de las constantes definidas en la clase, como: COVER_FILENAME, SYNOPSIS_FILENAME, etc.

        @raise Exception: si file se trata de un template de mako.
        """
        if file in EpubBaseFiles._TEMPLATES:
            raise Exception("{0} es un template de mako: use el método apropiado para obtener el xhtml")

        return EpubBaseFiles._getFile(file)

    @staticmethod
    def getSynopsis(synopsis):
        return EpubBaseFiles._getFile(EpubBaseFiles.SYNOPSIS_FILENAME, synopsis=synopsis)

    @staticmethod
    def getTitle(author, title, subtitle, editor, collectionName, subCollectionName, collectionVolume):
        return EpubBaseFiles._getFile(EpubBaseFiles.TITLE_FILENAME, author=author, title=title, subtitle=subtitle, editor=editor,
                                      collectionName=collectionName, subCollectionName=subCollectionName, collectionVolume=collectionVolume)

    @staticmethod
    def getInfo(originalTitle, author, publicationYear, translator, ilustrator, coverDesigner, coverModification, editor):
        return EpubBaseFiles._getFile(EpubBaseFiles.INFO_FILENAME, originalTitle=originalTitle, author=author, publicationYear=publicationYear,
                                      translator=translator, ilustrator=ilustrator, coverDesigner=coverDesigner,
                                      coverModification=coverModification, editor=editor)

    @staticmethod
    def getDedication(dedication):
        return EpubBaseFiles._getFile(EpubBaseFiles.DEDICATION_FILENAME, dedication=dedication)

    @staticmethod
    def getAuthor(authorBiography, title, imageName):
        return EpubBaseFiles._getFile(EpubBaseFiles.AUTHOR_FILENAME, authorBiography=authorBiography, title=title, imageName=imageName)

    @staticmethod
    def generateTextSectionName(sectionNumber):
        return "Section{0:04}.xhtml".format(sectionNumber)

    @staticmethod
    def generateAuthorImageFileName(imageNumber):
        if imageNumber == 0:
            return EpubBaseFiles.AUTHOR_IMAGE_FILENAME

        return EpubBaseFiles.AUTHOR_IMAGE_FILENAME[:-4] + str(imageNumber) + EpubBaseFiles.AUTHOR_IMAGE_FILENAME[-4:]

    @staticmethod
    def generateAuthorFileName(authorNumber):
        if authorNumber == 0:
            return EpubBaseFiles.AUTHOR_FILENAME

        return EpubBaseFiles.AUTHOR_FILENAME[:-6] + str(authorNumber) + EpubBaseFiles.AUTHOR_FILENAME[-6:]

    @staticmethod
    def _getFile(fileName, **kwargs):
        if fileName not in EpubBaseFiles._FILES:
            EpubBaseFiles._loadEpubBaseFile(fileName)

        file = EpubBaseFiles._FILES[fileName]
        return file.render(**kwargs) if kwargs else file

    @staticmethod
    def _loadEpubBaseFile(fileName):
        if fileName in EpubBaseFiles._TEMPLATES:
            filePath = os.path.join(config.EPUBBASE_FILES_DIR_PATH, fileName)
            newFilePath = filePath.replace(".xhtml", ".mako")
            EpubBaseFiles._FILES[fileName] = mako.template.Template(filename=newFilePath, input_encoding="utf-8", output_encoding="utf-8")
        else:
            filePath = os.path.join(config.EPUBBASE_FILES_DIR_PATH, fileName)
            with open(filePath, "rb") as file:
                EpubBaseFiles._FILES[fileName] = file.read()