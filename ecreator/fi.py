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
import sys

from lxml import etree

from ecreator import ebook_data


class Fi:

    VALID_IMAGE_TYPES = ("png", "jpg", "jpeg", "gif")

    _XHTML_NS = "http://www.w3.org/1999/xhtml"
    _DOCTYPE = ('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"\n'
                ' "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n')
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
        """
        Corrige todos los tags "h" en los archivos de texto y genera además la lista de títulos.
        En la conversión al FI no supongo que los títulos están correctamente anidados, es más, probablemente
        estén mal (sobre todo si el archivo de origen fue un docx...). Por eso con este método debo procesar
        los títulos y corregir los tags "h" de manera acorde.

        @param ebookSections: una lista de File con los archivos de texto del ebook.

        @return: una lista de Title con la toc.
        """
        # Contiene todos los títulos de primer nivel del libro (los h1). Es una lista de Title.
        ebookRootTitles = []
        
        # Indica cuál fue el nivel de heading anterior procesado
        previousHeadingNumber = 0

        # Representa cuál es, en un momento dado, el nro de heading de primer nivel, es
        # decir, el que vendría a ser una entrada de primer nivel en la toc.
        # Puede darse una toc así:
        #               t3
        #               t3
        #           t2
        #           t2
        #       t1
        #       t1
        # Como se ve, los dos primeros t3 vendrían a ser en realidad t1, pero están corridos. Lo mismo
        # con los t2. No puedo suponer que los t1 van a ser siempre mi título de nivel 1. Incluso puede darse
        # el caso de una toc que no tenga t1, sino que absolutamente todos los títulos estén corridos.
        headingBase = sys.maxsize
        
        for ebookSection in ebookSections:
            sectionXml = etree.XML(ebookSection.content)
            body = self._xpath(sectionXml, "/x:html/x:body")[0]
            headings = self._xpath(body, "x:h1 | x:h2 | x:h3 | x:h4 | x:h5 | x:h6")

            for heading in headings:
                # Necesito obtener el nivel de heading
                currentHeadingNumber = int(heading.tag[heading.tag.rindex("h") + 1:])

                titleLocation = "{0}#{1}".format(ebookSection.name, heading.get("id"))
                titleText = self._getAllText(heading, "{{{0}}}a".format(Fi._XHTML_NS)).strip()

                if currentHeadingNumber < headingBase:
                    headingBase = currentHeadingNumber

                # Si es un heading de primer nivel, entonces ésta es una entrada en la toc de primer nivel.
                if currentHeadingNumber == headingBase:
                    title = ebook_data.Title(titleLocation, titleText)
                    ebookRootTitles.append(title)

                    # Esto es un stack que contiene una tupla con dos elementos: el primero representa un objeto
                    # Title, y el segundo es un int con el nivel de título asociado al Title. El stack me sirve para
                    # manejar el anidamiento de títulos correctamente, y siempre el primer elemento que voy a pushear
                    # va a ser un título de primer nivel.
                    titlesStack = [(title, currentHeadingNumber)]
                else:
                    if currentHeadingNumber < previousHeadingNumber:                                            
                        # Si el nivel de título actual es menor al anterior, debo sacar los títulos necesarios
                        # de mi pila para poner el título actual en el nivel que corresponde. Ejemplo:
                        #           1
                        #               2
                        #                   3
                        #                       4
                        # Dada una toc como la de arriba, si ahora tengo que insertar un título de nivel 2, debo ir
                        # comparando el 2 con cada uno de los niveles de títulos que están en la pila. Mientras mi
                        # título 2 sea menor o igual al que se encuentra en la pila, debo hacer un pop.
                        # De esta manera me queda en la cima de la pila el título padre en el cual debo insertar mi
                        # título 2 hijo.
                        while currentHeadingNumber <= titlesStack[-1][1]:
                            titlesStack.pop()
                    elif currentHeadingNumber == previousHeadingNumber:
                        # Si el nivel de título actual es igual al anterior procesado, significa que los títulos son
                        # hermanos, o sea, que tienen el mismo padre, por lo que me basta hacer un solo pop en la pila
                        # para insertarlo en el lugar correcto. Ej:
                        #                   4
                        #                       5
                        # Si tengo que insertar un nuevo título 5 en la toc de arriba, debo sacar el título 5 de la
                        # cima de la pila para que quede el título 4 en la cima.
                        titlesStack.pop()
                    
                    # Inserto el título cuando no es un título de primer nivel.
                    childTitle = titlesStack[-1][0].addTitle(titleLocation, titleText)
                    titlesStack.append((childTitle, currentHeadingNumber))

                # Una vez procesado el heading, corrijo el tag en la sección correspondiente.
                heading.tag = "h{0}".format(len(titlesStack))
                previousHeadingNumber = currentHeadingNumber

            # Una vez procesados todoos los títulos de la sección, actualizo su contenido, con todos los headings ya
            # corregidos.
            ebookSection.content = etree.tostring(sectionXml,
                                                  encoding="utf-8",
                                                  xml_declaration=True,
                                                  doctype=Fi._DOCTYPE).decode("utf-8")

        return ebookRootTitles

    def _getAllText(self, node, ignorableNodes=None):
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