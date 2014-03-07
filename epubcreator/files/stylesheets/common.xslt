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

<!--***********************************************************************************************
	Inserta una referencia a una nota.

	noteNumber: el número de la nota.
	***********************************************************************************************-->
<xsl:template name="insertNoteReference">
	<xsl:param name="noteNumber"/>

	<a id="rf{$noteNumber}" href="../Text/notas.xhtml#nt{$noteNumber}"><sup>[<xsl:value-of select="$noteNumber"/>]</sup></a>
</xsl:template>

<!--***********************************************************************************************
	Inserta el retorno de nota.
	Debe llamarse al template luego de procesar el último párrafo del contenido de una nota al
	pie. Es decir, el retorno de nota debe ir dentro del último párrafo de la nota (y debe
	colocarse al final).

	sectionName:	el nombre de la sección a la cual se debe retornar.
	noteId:			el id de la nota a la cual se debe retornar.
	***********************************************************************************************-->
<xsl:template name="insertNoteReturn">
	<xsl:param name="sectionName"/>
	<xsl:param name="noteId"/>
	
	<!--El retorno de notas tiene un pequeño espacio que lo separa del final del texto-->
	<xsl:text> </xsl:text>
	
	<a href="../Text/{$sectionName}#{$noteId}">&lt;&lt;</a>
</xsl:template>

<!--***********************************************************************************************
	Inserta el número de nota.
	El template debe llamarse al momento de procesar el primer párrafo del contenido de una nota
	al pie. Es decir, el número de nota debe ir solamente dentro del primer párrafo de la nota.

	noteNumber: el número de la nota.
	***********************************************************************************************-->
<xsl:template name="insertNoteNumber">
	<xsl:param name="noteNumber"/>

	<a id="nt{$noteNumber}"></a>
	<sup>
		<xsl:text>[</xsl:text><xsl:value-of select="$noteNumber"/><xsl:text>]</xsl:text>
	</sup>
</xsl:template>

</xsl:stylesheet>