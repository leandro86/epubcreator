from epubcreator.converters import xml_utils

NAMESPACES = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
              "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
              "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
              "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
              "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
              "rels": "http://schemas.openxmlformats.org/package/2006/relationships",
              "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
              "wps": "http://schemas.microsoft.com/office/word/2010/wordprocessingShape"}


def getRunFormats(run):
    rpr = run.find("w:rPr", namespaces=NAMESPACES)
    return getFormats(rpr)


def getFormats(node, processSubAndSup=True):
    """
    Dado un nodo w:rPr o w:pPr, convierte los formatos que contiene y los retorna.

    @param node: el lxml Element que contiene los nodos hijos con los formatos.
    @param processSubAndSup: indica si deben convertirse los subíndices y superíndices.

    @return: una lista de string con los formatos convertidos.
    """
    formats = []

    if node is not None:
        for child in node:
            if child.tag.endswith("}b"):
                formats.append("strong")
            elif child.tag.endswith("}i"):
                formats.append("em")
            elif child.tag.endswith("}u"):
                formats.append("ins")
            elif child.tag.endswith("}vertAlign") and processSubAndSup:
                val = xml_utils.getAttr(child, "w:val", NAMESPACES)
                if val == "superscript":
                    formats.append("sup")
                elif val == "subscript":
                    formats.append("sub")

    return formats


def isPageBreakOnBeginning(paragraph):
    return bool(xml_utils.xpath(paragraph, "w:r[1][w:br/@w:type = 'page'] or w:pPr/w:pageBreakBefore", NAMESPACES))


def isPageBreakOnEnd(paragraph):
    return bool(xml_utils.xpath(paragraph, "w:r[w:br/@w:type = 'page' and position() > 1]", NAMESPACES))


def getNextParagraph(paragraph):
    nextParagraph = xml_utils.xpath(paragraph, "following-sibling::w:p[1]", NAMESPACES)
    return nextParagraph[0] if nextParagraph else None


def getPreviousParagraph(paragraph):
    previousParagraph = xml_utils.xpath(paragraph, "preceding-sibling::w:p[1]", NAMESPACES)
    return previousParagraph[0] if previousParagraph else None


def getNextRun(run):
    nextRun = xml_utils.xpath(run, "following-sibling::w:r[1]", NAMESPACES)
    return nextRun[0] if nextRun else None


def getPreviousRun(run):
    previousRun = xml_utils.xpath(run, "preceding-sibling::w:r[1]", NAMESPACES)
    return previousRun[0] if previousRun else None