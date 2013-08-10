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

from lxml import etree


class Toc:
    
    TOC_NS = "http://www.daisy.org/z3986/2005/ncx/"
    
    def __init__(self):
        self._headItems = []
        self._metadataItems = []
        self._navPoints = []
    
    def addIdentifier(self, identifier):
        self._headItems.append(_HeadItem("uid", identifier))
    
    def addTitle(self, title):
        self._metadataItems.append(_MetadataItem("docTitle", title))
        
    def addNavPoint(self, ref, title):
        navPoint = NavPoint(ref, title)
        self._navPoints.append(navPoint)
        
        return navPoint
    
    def toXml(self):
        toc = etree.Element("{{{0}}}ncx".format(Toc.TOC_NS), {"version" : "2005-1"}, nsmap = {None : Toc.TOC_NS})

        # Agrego todos los playorders e ids de los navpoints
        playOrder = 1
        for navPoint in self._navPoints:
            playOrder = self._appendNavPointsPlayOrderAndId(navPoint, playOrder)
        
        tocHead = etree.SubElement(toc, "head")
        self._addRequiredTocHeadItems()      
        for headItem in self._headItems:
            tocHead.append(headItem.toElement())         
        
        for metadataItem in self._metadataItems:
            toc.append(metadataItem.toElement())   

        navMap = etree.SubElement(toc, "navMap")
        for navPoint in self._navPoints:
            navMap.append(navPoint.toElement())
    
        doctypeText = ('<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" '
                       '"http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">')
        return etree.tostring(toc, encoding = "utf-8", xml_declaration = True, doctype = doctypeText,
                              pretty_print = True)

    def _appendNavPointsPlayOrderAndId(self, navPoint, startPlayOrder):
        """
        Agrego los playorders e ids al navpoint pasado como parámetro, y recursivamente a todos sus navpoints
        hijos también.

        @param navPoint: un objeto NavPoint.
        @param startPlayOrder: el número de playorder desde el cual empezar a contar.

        @return: el próximo número de playorder válido.
        """
        navPoint.playOrder = startPlayOrder
        navPoint.navId = "navPoint-{0}".format(startPlayOrder)

        nextPlayOrder = startPlayOrder + 1
        for childNavPoint in navPoint.navPoints:
            nextPlayOrder = self._appendNavPointsPlayOrderAndId(childNavPoint, nextPlayOrder)

        return nextPlayOrder
    
    def _addRequiredTocHeadItems(self):
        self._headItems.append(_HeadItem("depth", "1"))
        self._headItems.append(_HeadItem("totalPageCount", "0"))
        self._headItems.append(_HeadItem("maxPageNumber", "0"))


class NavPoint:
        
    def __init__(self, ref, title):
        # Una lista de NavPoint con los navpoints hijos
        self.navPoints = []

        self.ref = "Text/{0}".format(ref)
        self.title = title

        # En el momento de generar el epub es cuando corrijo todos los playorders e ids. No puedo ir generando
        # estos valores a medida que voy agregando navpoints, porque hay muchas formas de que queden en estado
        # inconsistente si no voy agregando los navpoints ordenadamente.
        self.playOrder = 0
        self.navId = ""

    def addNavPoint(self, ref, title):
        navPoint = NavPoint(ref, title)
        self.navPoints.append(navPoint)

        return navPoint

    def toElement(self):
        navPoint = etree.Element("navPoint", {"id" : str(self.navId), "playOrder" : str(self.playOrder)})
        navLabel = etree.SubElement(navPoint, "navLabel")
        
        textElement = etree.SubElement(navLabel, "text")
        textElement.text = self.title
        
        etree.SubElement(navPoint, "content", {"src" : self.ref})
        
        for nvPoint in self.navPoints:
            navPoint.append(nvPoint.toElement())
        
        return navPoint                      


class _HeadItem:
    
    def __init__(self, name, content):
        self._name = name
        self._ref = content
    
    def toElement(self):
        return etree.Element("meta", {"name" : "dtb:{0}".format(self._name), "content" : self._ref})


class _MetadataItem:
    
    def __init__(self, tag, content):
        self._tag = tag
        self._ref = content

    def toElement(self):
        root = etree.Element(self._tag)
        textElement = etree.SubElement(root, "text")
        textElement.text = self._ref        
        return root
        