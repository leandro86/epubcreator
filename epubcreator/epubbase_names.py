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
IBOOKS_EMBEDDED_FONTS_FILENAME = "com.apple.ibooks.display-options.xml"


def generateTextSectionName(sectionNumber):
    return "Section{0:04}.xhtml".format(sectionNumber)