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

<xsl:param name="synopsis">Yo por bien tengo que cosas tan señaladas, y por ventura nunca oídas ni vistas, vengan a noticia de muchos y no se entierren en la sepultura del olvido, pues podría ser que alguno que las lea halle algo que le agrade, y a los que no ahondaren tanto los deleite.&#xa;Y a este propósito dice Plinio que no hay libro, por malo que sea, que no tenga alguna cosa buena; mayormente que los gustos no son todos unos, mas lo que uno no come, otro se pierde por ello.</xsl:param>

<xsl:template match="/">
	<html xmlns="http://www.w3.org/1999/xhtml">
		<head>
			<title></title>
			<link href="../Styles/style.css" rel="stylesheet" type="text/css" />
		</head>
		<body>	
			<p><xsl:text disable-output-escaping="yes">&amp;nbsp;</xsl:text></p>
			<xsl:comment> se usa el <xsl:text disable-output-escaping="yes">&amp;nbsp;</xsl:text> para evitar un bug de iBooks (iPad/iPhone/iPod) </xsl:comment>
				
			<div class="sinopsis">
				<xsl:for-each select="str:tokenize($synopsis, '&#xa;')">
					<p><xsl:value-of select="."></xsl:value-of></p>
				</xsl:for-each>		
			</div>
		</body>
	</html>
</xsl:template>

</xsl:stylesheet>