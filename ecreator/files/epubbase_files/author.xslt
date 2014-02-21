<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
				xmlns:str="http://exslt.org/strings"
				extension-element-prefixes="str"
				version="1.0">

<xsl:output method="xml" 
			doctype-public="-//W3C//DTD XHTML 1.1//EN"
			doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd" 
			standalone="no" 
			encoding="utf-8" 
			omit-xml-declaration="no" 
			indent="yes" 
			version="1.0"/>

<xsl:param name="authorBiography">NOMBRE DEL AUTOR. (Reikiavik, Islandia, 2013 - Terra III, 3096). Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc vel libero sed est ultrices elementum at vel lacus. Sed laoreet, velit nec congue pellentesque, quam urna pretium nunc, et ultrices nulla lacus non libero.&#xa;Integer eu leo justo, vel sodales arcu. Donec posuere nunc in lectus laoreet a rhoncus enim fermentum. Nunc luctus accumsan ligula eu molestie.</xsl:param>

<xsl:template match="/">
	<html xmlns="http://www.w3.org/1999/xhtml">
		<head>
			<title></title>
			<link href="../Styles/style.css" rel="stylesheet" type="text/css" />
		</head>
		<xsl:comment> este documento es opcional, debe eliminarse de ser innecesario junto con el documento autor.jpg de la carpeta de imágenes </xsl:comment><xsl:text>&#10;</xsl:text>

		<body>
			<h1 class="oculto" title="Autor"></h1>
			<xsl:comment> puede cambiarse a «Autora» o «Autores» de ser necesario </xsl:comment>

			<div class="vineta"><img alt="" height="40%" src="../Images/autor.jpg" /></div>	<xsl:comment> atención: por compatibilidad, este archivo de imagen no debe exceder los 600px de ancho ni haber sido guardado como jpeg «progresivo» </xsl:comment>

            <div class="autor">
                <xsl:variable name="paragraphs" select="str:tokenize($authorBiography, '&#xa;')"></xsl:variable>               
                
                <xsl:for-each select="$paragraphs">
                    <p><xsl:value-of select="."/></p>
                </xsl:for-each>
           </div>
		</body>
	</html>
</xsl:template>

</xsl:stylesheet>