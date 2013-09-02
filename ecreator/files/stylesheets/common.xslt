<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet	xmlns="http://www.w3.org/1999/xhtml"
				xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
				version="1.0">

<!--***********************************************************************************************
	Genera el nombre de una sección de texto para el epub.

	number:		el número de sección para el cual generar el nombre.

	Retorna el nombre generado para la sección.
	***********************************************************************************************-->
<xsl:template name="generateSectionName">
	<xsl:param name="number"/>
	
	<!--Me aseguro de que el número de sección sea de 4 caracteres, y que esté 
		paddeado con ceros a la izquierda-->	
	<xsl:variable name="sectionNumber" select="concat('000', $number)"/>
	<xsl:value-of select="concat('Section', substring($sectionNumber, string-length($number), 4), '.xhtml')"/>
</xsl:template>

<!--***********************************************************************************************
	Inserta un separador, que sirve para indicar las partes importantes del doc.

	text:	el texto del separador.
	***********************************************************************************************-->
<xsl:template name="insertSeparator">	
	<xsl:param name="text"/>
	
	<xsl:comment>[<xsl:value-of select="$text"/>]</xsl:comment>
</xsl:template>

<!--***********************************************************************************************
	Inserta un separador para distingur cuándo comienza una nueva sección de texto.

	number:		el número de la sección a insertar.
	***********************************************************************************************-->
<xsl:template name="startNewSection">
	<xsl:param name="number"/>
	
	<xsl:variable name="sectionName">
		<xsl:call-template name="generateSectionName">
			<xsl:with-param name="number" select="$number"/>
		</xsl:call-template>
	</xsl:variable>
	
	<xsl:call-template name="insertSeparator">
		<xsl:with-param name="text" select="$sectionName"/>
	</xsl:call-template>
</xsl:template>

<!--***********************************************************************************************
	Inserta el separador de la sección notas.
	***********************************************************************************************-->
<xsl:template name="startNotesSection">	
	<xsl:call-template name="insertSeparator">
		<xsl:with-param name="text" select="'notas.xhtml'"/>
	</xsl:call-template>
	<h1>Notas</h1>
</xsl:template>

<!--***********************************************************************************************
	Inserta el retorno de nota.

	sectionName:	el nombre de la sección a la cual se debe retornar.
	noteId:			el id de la nota a la cual se debe retornar.
	***********************************************************************************************-->
<xsl:template name="insertNoteReturn">
	<xsl:param name="sectionName"/>
	<xsl:param name="noteId"/>
	
	<a href="../Text/{$sectionName}#{$noteId}">&lt;&lt;</a>
</xsl:template>

<!--***********************************************************************************************
	Inserta una imagen.

	name: el nombre de la imagen a insertar.
	***********************************************************************************************-->
<xsl:template name="insertImage">
	<xsl:param name="name"/>

	<xsl:variable name="type">
		<xsl:value-of select="substring-after($name, '.')"/>
	</xsl:variable>

	<img src="../Images/{$name}">
		<xsl:attribute name="alt"><xsl:value-of select="$name"/></xsl:attribute>
	</img>
</xsl:template>

</xsl:stylesheet>