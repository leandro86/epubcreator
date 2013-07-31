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

<xsl:param name="dedication"/>

<xsl:template match="/">
	<html xmlns="http://www.w3.org/1999/xhtml">
		<head>
			<title></title>
			<link href="../Styles/style.css" rel="stylesheet" type="text/css" />
		</head>
		<xsl:comment> este documento es opcional, debe eliminarse de ser innecesario </xsl:comment>

		<body>
			<div class="dedicatoria">
				<xsl:choose>
					<xsl:when test="$dedication">		
						<xsl:for-each select="str:tokenize($dedication, '&#xa;')">
							<p><xsl:value-of select="."></xsl:value-of></p>
						</xsl:for-each>		
					</xsl:when>
					<xsl:otherwise>
						<p>Suspiró entonces mío Cid, de pesadumbre cargado, y comenzó a hablar así, justamente mesurado: «¡Loado seas, Señor, Padre que estás en lo alto! Todo esto me han urdido mis enemigos malvados».</p>
						<p class="salto05"><span class="versalita">ANÓNIMO</span></p>
					</xsl:otherwise>
				</xsl:choose>
			</div>
		</body>
	</html>
</xsl:template>

</xsl:stylesheet>