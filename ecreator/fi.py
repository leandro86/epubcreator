# -*- coding: utf-8 -*-

# Copyright (C) 2013 Leandro
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re

from lxml import etree

from ecreator import ebook_data


class Fi:

    _XHTML_NS = "http://www.w3.org/1999/xhtml"
    _SECTION_REGEX_SPLITTER = re.compile("<!--\[(\w+.xhtml)\]-->")

    def __init__(self, fi):
        """
        @param fi: un string con el contenido del fi.
        """
        self._fi = fi

    def parse(self):
        """
        Parsea el fi, generando las secciones y títulos del mismo.

        @return: una tupla con la lista de secciones y la lista de títulos.
        """
        ebookSections = []
        
        sections = Fi._SECTION_REGEX_SPLITTER.split(self._fi)

        htmlHead = sections[0]
        htmlTail = sections[-1]

        # Dado el split que hice, primero viene en la lista el nombre de la sección, y el siguiente
        # elemento es el contenido, por eso la recorro de a 2.
        for i in range(1, len(sections) - 2, 2):
            ebookSections.append(ebook_data.File(sections[i],
                                                 ebook_data.File.FILE_TYPE.TEXT,
                                                 htmlHead + sections[i + 1] + htmlTail))
        
        return ebookSections, self._parseTitles(ebookSections)

    def _parseTitles(self, ebookSections):
        # Contiene todos los títulos del primer nivel del libro (los h1). Es una lista de Title.
        ebookRootTitles = []
        
        # Indica cuál fue el heading anterior procesado
        previousHeadingNumber = 0
        
        for ebookSection in ebookSections:
            sectionXml = etree.XML(ebookSection.content)
            body = self._xpath(sectionXml, "/x:html/x:body")[0]
            headings = self._xpath(body, "x:h1 | x:h2 | x:h3 | x:h4 | x:h5 | x:h6")

            for heading in headings:
                # Necesito obtener el número de heading
                currentHeadingNumber = int(heading.tag[heading.tag.rindex("h") + 1:])

                titleLocation = "{0}#{1}".format(ebookSection.name, heading.get("id"))

                # Si el heading es 1, entonces es un título de primer nivel y debo guardarlo.
                if currentHeadingNumber == 1:
                    titleText = self._getAllText(heading, "{{{0}}}a".format(Fi._XHTML_NS)).strip()
                    title = ebook_data.Title(titleLocation, titleText)
                    ebookRootTitles.append(title)   
                                                         
                    # Necesito un stack para manejar el anidamiento de títulos correctamente. Este stack va a
                    # contener siempre, como primer elemento, algún h1. Es un stack de Title.
                    titlesStack = [title]                            
                else:
                    if currentHeadingNumber < previousHeadingNumber:                                            
                        # Si el h actual es menor al anterior, debo sacar los títulos necesarios de mi pila para
                        # poner el h actual en el nivel que corresponde. Ejemplo: si el h actual es 2, y el anterior
                        # es 4, debo sacar de la pila: el h4, el h3 y el h2, para poder insertar el h2 actual como
                        # hijo del h1.                        
                        for i in range((previousHeadingNumber - currentHeadingNumber) + 1):                        
                            titlesStack.pop()                            
                    elif currentHeadingNumber == previousHeadingNumber:
                        # Si el h actual es igual al anterior, debo sacar de mi pila de títulos el h que hay
                        # en la cima (que tiene el mismo nivel que el h actual), y reemplazarlo por el nuevo h.
                        # Ejemplo: si mi pila está así: [1, 2], no puedo permitir que quede: [1, 2, 2], ya que sino
                        # luego no voy a poder colocar correctamente un h menor al h anterior.                        
                        titlesStack.pop()      
                    
                    # Inserto finalmente el nuevo título.         
                    titlesStack.append(titlesStack[-1].addTitle(titleLocation, heading.text))
                previousHeadingNumber = currentHeadingNumber    
                                 
        return ebookRootTitles

    def _getAllText(self, node, ignorableNodes = ()):
        """
        Retorna todo el texto de un nodo, es decir, incluyendo el texto de todos los
        nodos descendientes.

        @param node: un lxml Element.
        @param ignorableNodes: una tupla de strings con el nombre (tag) de los nodos de los cuales
                               hay que ignorar su contenido.

        @return: un string con el texto del nodo.
        """
        text = ""

        if node.tag not in ignorableNodes:
            text = node.text or ""

            for child in node:
                text += self._getAllText(child, ignorableNodes)

        text += node.tail or ""

        return text

    def _xpath(self, element, xpath):
        return element.xpath(xpath, namespaces = {"x" : Fi._XHTML_NS})