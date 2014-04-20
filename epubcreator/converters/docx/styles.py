from lxml import etree

from epubcreator.misc import xml_utils
from epubcreator.converters.docx import utils


class Styles:
    def __init__(self, stylesXml):
        # Un diccionario donde:
        # key   ->  id del estilo.
        # value ->  una tupla de tres elementos: el nombre del estilo
        #                                        el nombre tal como debe ir en el epub al ser usado como clase, si es un estilo custom, sino None
        #                                        una lista de strings con los formatos que el estilo tiene aplicado
        self._stylesIdToName = self._readStyles(stylesXml)

    def hasParagraphHeadingStyle(self, paragraph):
        styleId = self.getParagraphStyleId(paragraph)
        return styleId and (self._stylesIdToName[styleId][0].startswith("heading") or self._stylesIdToName[styleId][0].startswith("Encabezado"))

    def getParagraphStyleId(self, paragraph):
        styleId = xml_utils.xpath(paragraph, "w:pPr/w:pStyle/@w:val", utils.NAMESPACES)
        return styleId[0] if styleId else None

    def getRunStyleId(self, run):
        styleId = xml_utils.xpath(run, "w:rPr/w:rStyle/@w:val", utils.NAMESPACES)
        return styleId[0] if styleId else None

    def getParagraphStyleName(self, paragraph):
        styleId = self.getParagraphStyleId(paragraph)
        return self._stylesIdToName[styleId][0] if styleId else None

    def getRunStyleName(self, run):
        styleId = self.getRunStyleId(run)
        return self._stylesIdToName[styleId][0] if styleId else None

    def getParagraphClassName(self, paragraph):
        """
        Retorna, si el w:p pasado como parámetro tiene un estilo asociado y dicho estilo es un
        estilo custom, el nombre de la clase correspondiente tal como debe ir en el epub. Caso contrario
        se retorna None.
        """
        styleId = self.getParagraphStyleId(paragraph)
        className = None

        if styleId:
            className = self._stylesIdToName[styleId][1]

        return className

    def getRunClassName(self, run):
        """
        Retorna, si el w:r pasado como parámetro tiene un estilo asociado y dicho estilo es un
        estilo custom, el nombre de la clase correspondiente tal como debe ir en el epub. Caso contrario
        se retorna None.
        """
        styleId = self.getRunStyleId(run)
        className = None

        if styleId:
            className = self._stylesIdToName[styleId][1]

        return className

    def getStyleFormats(self, styleId):
        return self._stylesIdToName[styleId][2]

    def _readStyles(self, stylesXml):
        xml = etree.parse(stylesXml)
        styles = {}

        for child in xml.getroot():
            if child.tag.endswith("}style"):
                attr = xml_utils.getAttr(child, "w:type", utils.NAMESPACES)
                if attr == "paragraph" or attr == "character":
                    styleId = xml_utils.getAttr(child, "w:styleId", utils.NAMESPACES)
                    styleName = xml_utils.xpath(child, "w:name/@w:val", utils.NAMESPACES)[0]

                    formatNode = xml_utils.find(child, "w:rPr" if attr == "character" else "w:pPr", utils.NAMESPACES)
                    # En los estilos, ignoro si tienen aplicado el formato subíndice o superíndice. Una de las
                    # razones es que abby finereader no parece utilizar este mecanismo al utilizar subs o sups, sino
                    # que utiliza directamente las etiquetas de formato en el run. Pero el motivo principal es que
                    # el word le aplica a las referencias a las notas un estilo con el formato superíndice y en este
                    # caso particular no debería procesarlos. Podría de alguna manera comprobar si el estilo es el
                    # que word usa para las referencias a las notas, y en ese caso ignorar el formato, pero esto
                    # solo me complicaría las cosas.
                    styles[styleId] = (styleName, self._styleNameToClassName(styleName), utils.getFormats(formatNode, False))

        return styles

    def _styleNameToClassName(self, styleName):
        className = None

        if styleName.startswith("epub_"):
            # Los estilos de tipo "vinculado" aparecen definido dos veces en styles.xml: una vez
            # con el nombre normal (párrafo) y la otra con el string " Car" al final (carácter).
            className = styleName[5:len(styleName) if not styleName.endswith(" Car") else -4]

        return className