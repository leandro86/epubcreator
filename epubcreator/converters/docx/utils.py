NAMESPACES = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
              "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
              "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
              "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
              "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
              "rels": "http://schemas.openxmlformats.org/package/2006/relationships",
              "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
              "wps": "http://schemas.microsoft.com/office/word/2010/wordprocessingShape",
              "ct": "http://schemas.openxmlformats.org/package/2006/content-types",
              "v": "urn:schemas-microsoft-com:vml"}

PAGE_BREAK_ON_BEGINNING = 0
PAGE_BREAK_ON_END = 1
NO_PAGE_BREAK = 2


def getDisabledFormats(node):
    """
    Dado un nodo w:rPr o w:pPr, retorna los formatos que están aplicados pero deshabilitados.

    @param node: un lxml Element.

    @return: una lista de string con los formatos.
    """
    disabledFormats = []

    for child in node:
        if child.tag.endswith("}b") and getAttr(child, "w:val") == "0":
            disabledFormats.append("strong")
        elif child.tag.endswith("}i") and getAttr(child, "w:val") == "0":
            disabledFormats.append("em")
        elif child.tag.endswith("}u") and getAttr(child, "w:val") == "none":
            disabledFormats.append("ins")

    return disabledFormats


def getFormats(node, processSubAndSup=True):
    """
    Dado un nodo w:rPr o w:pPr, convierte los formatos que contiene y los retorna.

    @param node: un lxml Element.
    @param processSubAndSup: indica si deben convertirse los subíndices y superíndices.

    @return: una lista de string con los formatos convertidos.
    """
    formats = []

    for child in node:
        if child.tag.endswith("}b") and getAttr(child, "w:val") != "0":
            formats.append("strong")
        elif child.tag.endswith("}i") and getAttr(child, "w:val") != "0":
            formats.append("em")
        elif child.tag.endswith("}u") and getAttr(child, "w:val") != "none":
            formats.append("ins")
        elif child.tag.endswith("}vertAlign") and processSubAndSup:
            val = getAttr(child, "w:val")
            if val == "superscript":
                formats.append("sup")
            elif val == "subscript":
                formats.append("sub")

    return formats


def getPageBreakPosition(paragraph):
    if xpath(paragraph, "w:pPr/w:pageBreakBefore"):
        return PAGE_BREAK_ON_BEGINNING

    runWithBreak = xpath(paragraph, "w:r[w:br/@w:type = 'page']")
    if runWithBreak:
        # Compruebo si arriba del run hay texto. De ser así, entiendo entonces que el salto de página se
        # encuentra al final del párrafo. Caso contrario (si no hay texto arriba del run), el salto de página
        # se encuentra al principio del párrafo.
        if xpath(runWithBreak[0], "preceding-sibling::*[descendant::w:t[normalize-space(text()) != '']]"):
            return PAGE_BREAK_ON_END
        else:
            return PAGE_BREAK_ON_BEGINNING
    else:
        return NO_PAGE_BREAK


def getNextParagraph(paragraph):
    nextParagraph = xpath(paragraph, "following-sibling::w:p[1]")
    return nextParagraph[0] if nextParagraph else None


def getPreviousParagraph(paragraph):
    previousParagraph = xpath(paragraph, "preceding-sibling::w:p[1]")
    return previousParagraph[0] if previousParagraph else None


def getNextRun(run):
    nextRun = xpath(run, "following-sibling::w:r[1]")
    return nextRun[0] if nextRun else None


def getPreviousRun(run):
    previousRun = xpath(run, "preceding-sibling::w:r[1]")
    return previousRun[0] if previousRun else None


def getListLevel(paragraph):
    level = xpath(paragraph, "w:pPr/w:numPr/w:ilvl/@w:val")
    return int(level[0]) if level else -1


def getImagesId(node):
    return xpath(node, "descendant::pic:pic/pic:blipFill/a:blip/@r:embed | descendant::v:imagedata/@r:id")


def hasText(node):
    t = xpath(node, "descendant::w:t[normalize-space() != ''][1]")
    return True if t else False


### ######################################################################################### ###
### Algunas funciones que facilitan el utilizar expresiones xpath con los namespaces del docx ###
### ######################################################################################### ###
def getAttr(node, attr):
    ns, name = attr.split(":")
    return node.get("{{{0}}}{1}".format(NAMESPACES.get(ns), name))


def xpath(node, path):
    return node.xpath(path, namespaces=NAMESPACES)


def find(node, path):
    return node.find(path, namespaces=NAMESPACES)


def getAllText(node):
    return "".join(xpath(node, "descendant::text()"))