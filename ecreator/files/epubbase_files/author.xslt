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

<xsl:param name="authorBiography">NOMBRE DEL AUTOR. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc vel libero sed est ultrices elementum at vel lacus. Sed laoreet, velit nec congue pellentesque, quam urna pretium nunc, et ultrices nulla lacus non libero. Integer eu leo justo, vel sodales arcu. Donec posuere nunc in lectus laoreet a rhoncus enim fermentum. Nunc luctus accumsan ligula eu molestie. Phasellus vitae elit in eros ornare tempor quis sed sapien. Aliquam eu nisl placerat mi scelerisque semper. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Nulla aliquam, turpis in volutpat tincidunt, nisl ipsum ultrices augue, eu pretium sapien lorem non nibh. Vestibulum accumsan placerat scelerisque.</xsl:param>

<xsl:template match="/">
	<html xmlns="http://www.w3.org/1999/xhtml">
		<head>
			<title></title>
			<link href="../Styles/style.css" rel="stylesheet" type="text/css" />
		</head>
		<xsl:comment> este documento es opcional, debe eliminarse de ser innecesario junto con el documento autor.jpg de la carpeta de imágenes </xsl:comment><xsl:text>&#10;</xsl:text>
		<xsl:comment> atención: por problemas de compatibilidad con algunos dispositivos, EN NINGÚN CASO los archivos de imágenes deben exceder los 300k de tamaño </xsl:comment>

		<body>
			<h1 class="oculto" title="Autor"></h1>
			<xsl:comment> puede cambiarse a «Autora» o «Autores» de ser necesario </xsl:comment>

			<p class="autorimg"><img alt="" height="100%" src="../Images/autor.jpg" /></p>

			<xsl:variable name="paragraphs" select="str:tokenize($authorBiography, '&#xa;')"></xsl:variable>
			<xsl:if test="$paragraphs[1]">				
				<p class="asangre"><xsl:value-of select="$paragraphs[1]"/></p>
			</xsl:if>
			
			<xsl:for-each select="$paragraphs[position() > 1]">
				<p><xsl:value-of select="."/></p>
			</xsl:for-each>
		</body>
	</html>
</xsl:template>

</xsl:stylesheet>