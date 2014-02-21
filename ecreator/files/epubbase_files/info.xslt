<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
				version="1.0">

<xsl:output method="xml" 
			doctype-public="-//W3C//DTD XHTML 1.1//EN"
			doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd" 
			standalone="no" 
			encoding="utf-8" 
			omit-xml-declaration="no" 
			indent="yes" 
			version="1.0"/>

<xsl:param name="originalTitle"></xsl:param>
<xsl:param name="author">Autor</xsl:param>
<xsl:param name="publicationYear"></xsl:param>
<xsl:param name="translator"></xsl:param>
<xsl:param name="ilustrator"></xsl:param>
<xsl:param name="coverDesigner"></xsl:param>
<xsl:param name="coverDesignOrTweak">Diseño</xsl:param>
<xsl:param name="editor">Editor</xsl:param>

<xsl:template match="/">
	<html xmlns="http://www.w3.org/1999/xhtml">
		<head>
			<title></title>
			<link href="../Styles/style.css" rel="stylesheet" type="text/css" />
		</head>
		<xsl:comment> rellenar los datos de la info que se consideren necesarios y borrar el resto </xsl:comment>
	
		<body>
			<div class="info">
				<xsl:if test="$originalTitle">
					<p>Título original: <em><xsl:value-of select="$originalTitle"/></em></p>
				</xsl:if>
							
				<p>
					<xsl:value-of select="$author"/>
					<xsl:if test="$publicationYear">
						<xsl:value-of select="concat(', ', $publicationYear)"/>
					</xsl:if>
				</p>
				
				<xsl:if test="$translator">
					<p>Traducción: <xsl:value-of select="$translator"/></p>
				</xsl:if>
				
				<xsl:if test="$ilustrator">
					<p>Ilustraciones: <xsl:value-of select="$ilustrator"/></p>
				</xsl:if>
				
				<xsl:if test="$coverDesigner">
					<p><xsl:value-of select="$coverDesignOrTweak"/> de cubierta: <xsl:value-of select="$coverDesigner"/></p>
					<xsl:comment> usar la palabra «Diseño» si la cubierta fue creada especialmente para esta edición; «Retoque» si es una adaptación de otra existente </xsl:comment>
				</xsl:if>
				
				<p class="salto10">Editor digital: <xsl:value-of select="$editor"/></p>
				<xsl:comment>&lt;p class="salto10"&gt;Primer editor: Editor1 (r1.0 a 1.x)&lt;/p&gt;</xsl:comment><xsl:text>&#10;</xsl:text>
				<xsl:comment>&lt;p&gt;Segundo editor: Editor2 (r2.0 a 2.x)&lt;/p&gt;</xsl:comment><xsl:text>&#10;</xsl:text>
				<xsl:comment>&lt;p&gt;Tercer editor: Editor3 (r3.0 a 3.x)&lt;/p&gt;</xsl:comment><xsl:text>&#10;</xsl:text>
				<xsl:comment>&lt;p&gt;Corrección de erratas: ColaboradorA, ColaboradorB y ColaboradorC&lt;/p&gt;</xsl:comment>
				
				<p>ePub base r1.1</p>
			</div>
            <div class="vineta"><img alt="" height="20%" src="../Images/ex_libris.png"/></div>            
		</body>
</html>
</xsl:template>

</xsl:stylesheet>