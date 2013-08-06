<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet	xmlns="http://www.w3.org/1999/xhtml"
				xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
				xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" 
				xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
				xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"
				xmlns:rels="http://schemas.openxmlformats.org/package/2006/relationships"
				xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"				
				xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
				exclude-result-prefixes="w a pic rels r mc" 
				version="1.0">

<xsl:output method="xml" 
			doctype-public="-//W3C//DTD XHTML 1.1//EN"
			doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd" 
			standalone="no" 
			encoding="utf-8" 
			omit-xml-declaration="no" 
			indent="yes" 
			version="1.0"/>

<!--***********************************************************************************************	
	Parámetros.
	***********************************************************************************************-->
<!--El path hacia el archivo footnotes.xml-->
<xsl:param name="footNotesXmlPath">footnotes_path</xsl:param>

<!--El path hacia el archivo styles.xml-->
<xsl:param name="stylesXmlPath">styles_path</xsl:param>

<!--El path hacia el archivo document.xml.rels-->
<xsl:param name="relsXmlPath">rels_path</xsl:param>

<!--Indica si deben ignorarse ("Y") o no ("N") los párrafos en blanco.
	En caso de "N", los párrafos en blanco se convierten a las clases del
	epub "salto10" o "salto25", según las siguientes reglas:
		Un párrafo en blanco:			"salto10"
		Dos o más párrafos en blanco:	"salto25"-->
<xsl:param name="ignoreEmptyParagraphs">Y</xsl:param>

<!--***********************************************************************************************	
	Variables globales.
	**********************************************************************************************-->
<xsl:variable name="footNotesDoc" select="document($footNotesXmlPath)"/>
<xsl:variable name="stylesDoc" select="document($stylesXmlPath)"/>
<xsl:variable name="relsDoc" select="document($relsXmlPath)"/>

<!--Una cosa es el id del estilo, y otra el nombre. En document.xml, se utiliza el id del estilo para referenciarlo.
	Cada estilo está especificado en styles.xml: su id, nombre, formato, estilo padre, etc. Necesito hacer
	un mapeo entre el id del estilo y su nombre.
	Como se ve, en ningún momento hago referencia styles.xml, eso es porque <key> no me permite 
	usar la función "document" ni variables tampoco. Por eso es que al momento de buscar un valor con la 
	función key(), necesito previamente	cambiar el contexto hacia styles.xml, utilizando un for-each.-->
<xsl:key name="styles" match="w:styles/w:style/w:name/@w:val" use="parent::w:name/parent::w:style/@w:styleId"></xsl:key>

<!--Me guardo el id de los estilos de todos los títulos, así me facilito el buscar párrafos con títulos más adelante.-->
<xsl:variable name="headings" select="$stylesDoc/w:styles/w:style[starts-with(w:name/@w:val, 'heading') or 
																  starts-with(w:name/@w:val, 'Encabezado')]/@w:styleId">
</xsl:variable>

<!--Necesito tener una referencia al documento principal para poder leer del mismo cuando
	me encuentro en otro contexto, por ejemplo, analizando el contenido de las notas en footnotes.xml-->
<xsl:variable name="mainDocument" select="/"></xsl:variable>

<!--***********************************************************************************************	
	Warnings. (Ninguno por ahora...)
	**********************************************************************************************-->
<xsl:variable name="WARNING_PREFIX">**DOCX_WARNING**</xsl:variable>

<xsl:variable name="NESTED_PARAGRAPH_WARNING">
	<xsl:value-of select="$WARNING_PREFIX"/>
	<xsl:text>Se encontró un párrafo anidado, que fue reemplazado por una etiqueta "span". Revise dicha etiqueta.</xsl:text>
</xsl:variable>

<xsl:variable name="SHAPE_WARNING">
	<xsl:value-of select="$WARNING_PREFIX"/>
	<xsl:text>Se encontró una figura geométrica. Este tipo de figuras no son imágenes, por lo que no pueden trasladarse al epub.</xsl:text>
</xsl:variable>

<xsl:variable name="INVALID_IMAGE_FORMAT_WARNING">
	<xsl:value-of select="$WARNING_PREFIX"/>
	<xsl:text>Se encontró una imagen con un formato no válido para un epub. </xsl:text>	
	<xsl:text>Revise la etiqueta "img", cuyo atributo "alt" es "Formato inválido".</xsl:text>
</xsl:variable>

<!--***********************************************************************************************	
	Procesa el documento principal.
	***********************************************************************************************-->
<xsl:template match="w:document">
	<html>
		<head>
			<title/>
			<link href="../Styles/style.css" rel="stylesheet" type="text/css"/>
		</head>
		<body>
			<!--Primera sección-->
			<xsl:call-template name="startNewSection">
				<xsl:with-param name="number" select="0"/>
			</xsl:call-template>
			
			<xsl:apply-templates/>
			
			<!--Luego de procesar todas las secciones, proceso las notas, si es que hay.-->
			<xsl:if test="$footNotesDoc/w:footnotes/w:footnote[not(@w:type)][1]">
				<xsl:call-template name="startNotesSection"/>
				<xsl:apply-templates select="w:body/w:p/w:r/w:footnoteReference" mode="content"/>
			</xsl:if>
		
		<xsl:call-template name="insertSeparator">
			<xsl:with-param name="text" select="'HTML_TAIL.xhtml'"/>
		</xsl:call-template>			
		</body>
	</html>
</xsl:template>

<!--***********************************************************************************************	
	Proceso el contenido de una nota al pie, es decir, los párrafos que se encuentran dentro del
	archivo 'foonotes.xml'.
	***********************************************************************************************-->
<xsl:template match="w:p[parent::w:footnote]">
	<!--En el archivo footnotes.xml cada nota al pie tiene un atributo id que las identifica. 
		Esto me permite a mí insertar el número de nota de forma sencilla.-->
	<xsl:variable name="noteNumber" select="parent::w:footnote/@w:id"/>

	<p>
		<!--Si es el primer párrafo, debo insertar el id de la nota-->
		<xsl:if test="not(preceding-sibling::w:p)">
			<a id="nota{$noteNumber}"></a>
			<sup>
				<xsl:text>[</xsl:text><xsl:value-of select="$noteNumber"/><xsl:text>]</xsl:text>
			</sup>
		</xsl:if>

		<xsl:apply-templates/>

		<!--Una vez procesado el contenido del párrafo actual, debo comprobar si es el último párrafo de la nota. De
			ser así, debo agregar entonces el link de retorno.-->
		<xsl:if test="not(following-sibling::w:p)">
			<!--Necesito obtener de alguna manera el número de sección donde se encuentra 
				la referencia a la nota actual.-->
			<!--TODO: no sé si esta es la forma más óptima. Lo que hago es buscar en el doc 
				principal, dónde está la referencia a la nota que estoy procesando. Luego llamo a 
				una función para contar la cantidad de saltos de páginas que hay antes de dicha referencia.-->
			<xsl:variable name="sectionNumber">
				<xsl:call-template name="countSectionsBefore">
					<xsl:with-param name="paragraph" select="$mainDocument/w:document/w:body/w:p[w:r/w:footnoteReference[@w:id = $noteNumber]]"/>
				</xsl:call-template>
			</xsl:variable>	
								
			<xsl:variable name="sectionName">
				<xsl:call-template name="generateSectionName">
					<xsl:with-param name="number" select="$sectionNumber"/>
				</xsl:call-template>
			</xsl:variable>
			
			<!--El retorno de notas tiene un pequeño espacio que lo separa del final de párrafo...-->
			<xsl:text> </xsl:text>
			
			<xsl:call-template name="insertNoteReturn">
				<xsl:with-param name="sectionName" select="$sectionName"/>
				<xsl:with-param name="noteId" select="concat('nota', $noteNumber, '-ref')"/>
			</xsl:call-template>
		</xsl:if>
	</p>
</xsl:template>

<!--***********************************************************************************************	
	Procesa los párrafos. Dependiendo de si se trata de un párrafo común o un título, se llama al
	template correspondiente para que los procese.
	Hubiera sido mejor hacer un template que matchee los títulos por un lado, y otro para los 
	párrafos. Sin embargo, no puedo hacer esto: hasta no haber leído el archivo styles.xml, no sé
	cuál va a ser el nombre de los estilos de los títulos, por eso debo guardarlos en una variable.
	Pero resulta que en el "match" de un template no puedo utilizar variables... al menos en
	xslt 1.0.
	***********************************************************************************************-->
<xsl:template match="w:p">
	<xsl:variable name="style">
		<xsl:variable name="currentStyleId" select="w:pPr/w:pStyle/@w:val"/>
		<!--Obtengo el nombre del estilo a partir del id, haciendo un cambio de contexto hacia
			styles.xml. (Ver arriba en la definición de "styles" por qué es necesario el
			cambio de contexto.)-->
		<xsl:for-each select="$stylesDoc">
			<xsl:value-of select="key('styles', $currentStyleId)"/>
		</xsl:for-each>			
	</xsl:variable>

	<xsl:choose>		
		<xsl:when test="starts-with($style, 'Encabezado') or starts-with($style, 'heading')">	
			<xsl:call-template name="processHeading">
				<xsl:with-param name="style" select="$style"/>
			</xsl:call-template>
		</xsl:when>
		<xsl:otherwise>
			<xsl:call-template name="processParagraph">
				<xsl:with-param name="style" select="$style"/>
			</xsl:call-template>		
		</xsl:otherwise>
	</xsl:choose>
	
	<xsl:call-template name="checkForSectionBreak">
		<xsl:with-param name="paragraph" select="."/>
	</xsl:call-template>
</xsl:template>

<!--***********************************************************************************************
	Procesa los headings. Los títulos en docx no tienen ningún tag especial, sino que solamente
	un estilo particular aplicado al párrafo me indica que se trata de un título.

	style:	el estilo aplicado al párrafo actual.
	***********************************************************************************************-->
<xsl:template name="processHeading">
	<xsl:param name="style"/>
	
	<xsl:variable name="headingNumber"><xsl:value-of select="substring($style, string-length($style), 1)"/></xsl:variable>
	<xsl:choose>
		<!--Si el número de heading es mayor a 6, no lo proceso como heading, sino como párrafo común.-->
		<xsl:when test="$headingNumber > 6">
			<xsl:call-template name="processParagraph">
				<xsl:with-param name="style" select="$style"/>
			</xsl:call-template>
		</xsl:when>
		<xsl:otherwise>
			<xsl:if test="w:r/w:t[normalize-space(text()) != '']">
				<xsl:element name="h{$headingNumber}">
					<xsl:variable name="headingsBeforeCount">
						<xsl:call-template name="countHeadingsBefore">
							<xsl:with-param name="paragraph" select="."/>
						</xsl:call-template>
					</xsl:variable>
					
					<!--Sumo 1, porque sino los id's me empiezan de 0 a contar...-->
					<xsl:attribute name="id">heading_id_<xsl:value-of select="$headingsBeforeCount + 1"/></xsl:attribute>	
					
					<xsl:apply-templates/>
				</xsl:element>		
			</xsl:if>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<!--***********************************************************************************************	
	Proceso los párrafos comunes.

	style: el estilo aplicado al párrafo actual.
	***********************************************************************************************-->
<xsl:template name="processParagraph">
	<xsl:param name="style"/>

	<xsl:variable name="tag">
		<xsl:choose>
			<!--Si se trata de un párrafo anidado utilizo el tag "span".-->
			<xsl:when test="ancestor::w:p[1]">
				<xsl:value-of select="'span'"/>
				<xsl:message><xsl:value-of select="$NESTED_PARAGRAPH_WARNING"/></xsl:message>
			</xsl:when>
			<xsl:otherwise>p</xsl:otherwise>
		</xsl:choose>
	</xsl:variable>	
	
	<xsl:choose>
		<xsl:when test="normalize-space(descendant::w:t) != ''">		
			<xsl:variable name="classValue">
				<!--Agrego la clase 'salto', dependiendo de si debo procesar los párrafos en blanco y de cuántos
					párrafos en blanco hay antes del actual que estoy procesando.-->
				<xsl:if test="$ignoreEmptyParagraphs = 'N' and preceding-sibling::w:p[1][not(w:r/w:t[normalize-space(text()) != ''])]">
					<xsl:text>salto</xsl:text>						
					<xsl:choose>
						<xsl:when test="preceding-sibling::w:p[2][not(w:r/w:t[normalize-space(text()) != ''])]">25 </xsl:when>
						<xsl:otherwise>10 </xsl:otherwise>
					</xsl:choose>
				</xsl:if>
				<!--Compruebo si hay algún estilo propio-->
				<xsl:if test="starts-with($style, 'epub_')">
					<xsl:value-of select="substring($style, 6)"/>
				</xsl:if>
			</xsl:variable>
			
			<xsl:element name="{$tag}">
				<xsl:if test="$classValue != ''">
					<xsl:attribute name="class"><xsl:value-of select="$classValue"/></xsl:attribute>									
				</xsl:if>
				
				<xsl:apply-templates/>	
			</xsl:element>
		</xsl:when>
		<xsl:when test="descendant::pic:pic">
			<xsl:element name="{$tag}">
				<xsl:attribute name="class">ilustra</xsl:attribute>
				<xsl:apply-templates/>
			</xsl:element>
		</xsl:when>
</xsl:choose>
</xsl:template>

<!--***********************************************************************************************
	Procesa los 'runs'.
	***********************************************************************************************-->
<xsl:template match="w:r">
	<xsl:variable name="previousFormats">
		<xsl:call-template name="transformRunFormats">
			<xsl:with-param name="run" select="preceding-sibling::w:r[1]"/>
		</xsl:call-template>
	</xsl:variable>	
	<xsl:variable name="nextFormats">
		<xsl:call-template name="transformRunFormats">
			<xsl:with-param name="run" select="following-sibling::w:r[1]"/>
		</xsl:call-template>
	</xsl:variable>	
	<xsl:variable name="currentFormats">
		<xsl:call-template name="transformRunFormats">
			<xsl:with-param name="run" select="."/>
		</xsl:call-template>
	</xsl:variable>
	
	<xsl:if test="$currentFormats != $previousFormats">
		<xsl:call-template name="openFormats">
			<xsl:with-param name="formats" select="$currentFormats"/>
		</xsl:call-template>
	</xsl:if>
	
	<xsl:apply-templates/>
	
	<xsl:if test="$currentFormats != $nextFormats">
		<xsl:call-template name="closeFormats">
			<xsl:with-param name="formats" select="$currentFormats"/>
		</xsl:call-template>
	</xsl:if>
</xsl:template>

<!--***********************************************************************************************
	Procesa una referencia a una nota al pie.
	***********************************************************************************************-->
<xsl:template match="w:footnoteReference">
	<xsl:variable name="noteNumber" select="./@w:id"/>
	<a id="nota{$noteNumber}-ref" href="../Text/notas.xhtml#nota{$noteNumber}"><sup>[<xsl:value-of select="$noteNumber"/>]</sup></a>
</xsl:template>

<!--***********************************************************************************************
	Procesa el contenido de una nota al pie.
	***********************************************************************************************-->
<xsl:template match="w:footnoteReference" mode="content">
	<xsl:element name="div">
		<xsl:attribute name="class">nota</xsl:attribute>
			<xsl:apply-templates select="$footNotesDoc/w:footnotes/w:footnote[@w:id = current()/@w:id]"/>		
	</xsl:element>	
</xsl:template>

<!--***********************************************************************************************
	Procesa el texto propiamente dicho.
	***********************************************************************************************-->
<xsl:template match="w:t">
	<xsl:value-of select="."/>
</xsl:template>

<!--***********************************************************************************************
	Procesa las imágenes.
	***********************************************************************************************-->
<xsl:template match="pic:pic">
	<!--Las imágenes en document.xml contienen un id, que hace referencia a document.xml.rels.
		En dicho archivo se encuentra el path dentro del docx donde se encuentra físicamente la imagen.
		Las imágenes parecen estar siempre dentro del dir "media", por lo que solamente extraigo el
		nombre de la imagen.-->
	<xsl:variable name="rId">
		<xsl:value-of select="pic:blipFill/a:blip/@r:embed"/>	
	</xsl:variable>
	
	<xsl:variable name="imageName">
		<xsl:value-of select="substring-after($relsDoc/rels:Relationships/rels:Relationship[@Id = $rId]/@Target, 'media/')"/>
	</xsl:variable>
	
	<xsl:variable name="imageType">
		<xsl:value-of select="substring-after($imageName, '.')"/>
	</xsl:variable>
	
	<img src="../Images/{$imageName}">
		<xsl:variable name="altValue">
			<xsl:choose>		
				<xsl:when test="$imageType = 'png' or $imageName = 'jpg' or $imageName = 'jpeg' or $imageName = 'gif'">
					<xsl:value-of select="$imageName"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:text>Formato inválido</xsl:text>
					<xsl:message><xsl:value-of select="$INVALID_IMAGE_FORMAT_WARNING"/></xsl:message>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<xsl:attribute name="alt"><xsl:value-of select="$altValue"/></xsl:attribute>
	</img>
</xsl:template>


<xsl:template match="mc:AlternateContent">
	<xsl:message><xsl:value-of select="$SHAPE_WARNING"/></xsl:message>
	
	<!--Sigo aplicando templates, porque el shape probablemente tenga texto dentro, y debo procesarlo.-->
	<xsl:apply-templates/>
</xsl:template>

<!--***********************************************************************************************
	Los shapes y cuadros de texto tienen dos implementaciones: una actual, y otra por 
	compatiblidad anterior. Ambas se usan en el docx. Debo ignorar la versión para compatiblidad, 
	sino voy a obtener texto por duplicado (en el caso de un shape que contenga texto, por ej.).
	***********************************************************************************************-->
<xsl:template match="mc:Fallback">
</xsl:template>

<!--***********************************************************************************************
	Sobreescribo el template por defecto que procesa texto. 
	Solamente me interesa el texto de los elementos "t", no el resto. Por ej, un shape en el docx
	viene representado por varios elementos, uno de ellos es la posición relativa al párrafo, que se
	especifica así, por ej: "<wp:posOffset>608816</wp:posOffset>". Ese texto no debo procesarlo.
	Quién sabe cuántas cosas parecidas así me tiene reservadas el formato docx, así que mejor 
	cortar por lo sano.	
	***********************************************************************************************-->
<xsl:template match="text()">
</xsl:template>



<!--*************************************************************************************************-->
<!--****************************	Templates que no responden a objetos ****************************-->
<!--*************************************************************************************************-->



<!--***********************************************************************************************
	Genera todos los tags de apertura para los formatos pasados como parámetros.

	formats: un string que contiene una representación de formatos.
	***********************************************************************************************-->
<xsl:template name="openFormats">
	<xsl:param name="formats"/>
		
	<xsl:if test="substring($formats, 1, 1)='*'">
		<xsl:text disable-output-escaping="yes">&lt;strong&gt;</xsl:text>
	</xsl:if>
	<xsl:if test="substring($formats, 2, 1)='*'">
		<xsl:text disable-output-escaping="yes">&lt;em&gt;</xsl:text>
	</xsl:if>
	<xsl:if test="substring($formats, 3, 1)='*'">
		<xsl:text disable-output-escaping="yes">&lt;sup&gt;</xsl:text>
	</xsl:if>
	<xsl:if test="substring($formats, 4, 1)='*'">
		<xsl:text disable-output-escaping="yes">&lt;sub&gt;</xsl:text>
	</xsl:if>
	<xsl:if test="substring($formats, 5, 1)='*'">
		<xsl:text disable-output-escaping="yes">&lt;ins&gt;</xsl:text>
	</xsl:if>
</xsl:template>

<!--***********************************************************************************************
	Genera todos los tags de cierre para los formatos pasados como parámetros.

	formats: un string que contiene una representación de formatos.
	***********************************************************************************************-->
<xsl:template name="closeFormats">
	<xsl:param name="formats"/>
		
	<xsl:if test="substring($formats, 5, 1)='*'">
		<xsl:text disable-output-escaping="yes">&lt;/ins&gt;</xsl:text>
	</xsl:if>
	<xsl:if test="substring($formats, 4, 1)='*'">
		<xsl:text disable-output-escaping="yes">&lt;/sub&gt;</xsl:text>
	</xsl:if>
	<xsl:if test="substring($formats, 3, 1)='*'">
		<xsl:text disable-output-escaping="yes">&lt;/sup&gt;</xsl:text>
	</xsl:if>
	<xsl:if test="substring($formats, 2, 1)='*'">
		<xsl:text disable-output-escaping="yes">&lt;/em&gt;</xsl:text>
	</xsl:if>
	<xsl:if test="substring($formats, 1, 1)='*'">
		<xsl:text disable-output-escaping="yes">&lt;/strong&gt;</xsl:text>
	</xsl:if>
</xsl:template>

<!--***********************************************************************************************
	Convierte los formatos de un run en una representación de string.

	run:	el nodo "r" (run) del cual buscar los formatos.

	Retorna un string de 5 caracteres, donde un "-" significa ausencia de estilo, y "*" significa
	que ese estilo está aplicado al run. Los 5 caracteres representan, en orden:
		1-	Negrita
		2-	Itálica
		3-	Superíndice
		4-	Subíndice
		5-	Subrayado
	Ejemplo: "*-*-*", significa que el run tiene aplicado los estilos: negrita, superíndice y
					  subrayado.
	***********************************************************************************************-->	
<xsl:template name="transformRunFormats">
	<xsl:param name="run"/>	

	<!--TODO: por ahora, esto lo dejo así. No encontré la forma todavía de poder abrir y cerrar los tags
		de formato de manera elegante. Es muy difícil hacerlo sin poder mantener algún tipo de estado, algo
		que me indique qué formatos siguen abierto de runs anteriores, así puedo cerrar todos los anidamientos
		de manera acorde. Me limité a copiar la solución que usó tarloth en su planilla, que reconstruye de
		manera elegante los tags en la mayoría de los casos (cuando el formato de los runs que se comparan es
		EXACTAMENTE el mismo)-->

	<xsl:choose>
		<xsl:when test="not($run[w:rPr])">
			<xsl:text>-----</xsl:text>
		</xsl:when>				
		<xsl:otherwise>
			<xsl:variable name="style" select="$run/w:rPr"/>			
			<!--Negrita-->
			<xsl:choose>
				<xsl:when test="$style/w:b">*</xsl:when>
				<xsl:otherwise>-</xsl:otherwise>
			</xsl:choose>
			<!--Itálica-->
			<xsl:choose>
				<xsl:when test="$style/w:i">*</xsl:when>
				<xsl:otherwise>-</xsl:otherwise>
			</xsl:choose>
			<!--Superíndice-->
			<xsl:choose>
				<xsl:when test="$style/w:vertAlign/@w:val='superscript'">*</xsl:when>
				<xsl:otherwise>-</xsl:otherwise>
			</xsl:choose>
			<!--Subíndice-->
			<xsl:choose>
				<xsl:when test="$style/w:vertAlign/@w:val='subscript'">*</xsl:when>
				<xsl:otherwise>-</xsl:otherwise>
			</xsl:choose>
			<!--Subrayado-->
			<xsl:choose>
				<xsl:when test="$style/w:u">*</xsl:when>
				<xsl:otherwise>-</xsl:otherwise>
			</xsl:choose>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

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
	Comprueba si hay algún salto de página, y de ser así empieza una nueva sección.
	
	paragraph:	el párrafo en el cual se debe comprobar si hay un salto de página.
	***********************************************************************************************-->
<xsl:template name="checkForSectionBreak">
	<xsl:param name="paragraph"/>

	<xsl:if test="$paragraph/w:r[w:br/@w:type = 'page'] or $paragraph/following-sibling::w:p[1]/w:pPr/w:pageBreakBefore">
		<xsl:variable name="sectionsBeforeCount">	
			<xsl:call-template name="countSectionsBefore">
				<xsl:with-param name="paragraph" select="."/>
			</xsl:call-template>
		</xsl:variable>
		
		<xsl:call-template name="startNewSection">
			<!--Sumo uno, porque al principio de todoo agregué ya agregué la section 0.-->
			<xsl:with-param name="number" select="$sectionsBeforeCount + 1"/>
		</xsl:call-template>
	</xsl:if>
</xsl:template>

<!--***********************************************************************************************
	Cuenta la cantidad de saltos de páginas anteriores a algún element 'p'.

	paragraph:	el elemento 'p' hasta donde contar los saltos de páginas.

	Retorna el número de saltos de páginas antes del elemento 'p' pasado como parámetro.
	***********************************************************************************************-->
<xsl:template name="countSectionsBefore">
	<xsl:param name="paragraph"/>
	
	<!--Debo tener cuidado acá, porque según parece, word y libreoffice utilizan dos formas distintas
		de representar los saltos de página: word usa el br, y libreoffice el pageBreakBefore. El 
		problema es que el br indica que hay un salto de página luego del párrafo actual, y por ahora
		he visto que se lo pone al final del párrafo; el pageBreakBefore indica que hay un salto
		de página antes del párrafo actual, y se lo pone al principio del párrafo. Puede darse
		tranquilamente el caso de tener ambos tipos de saltos en el documento, y el siguiente ejemplo
		me genera un problema:
				<p>
					<t>texto</t>
					<r>
						<br type='page'/>
					</r>
				<p>
				<p>
					<pPr>
						<pageBreakBefore/>
					<pPr>
				</p>
		Como se ve en el ejemplo, no puedo contabilizar lo anterior como dos saltos de página, sino que
		en realidad es uno solo.-->
	<xsl:variable name="pWithBr" select="$paragraph/preceding-sibling::w:p[w:r/w:br[@w:type = 'page']]"/>
	<xsl:variable name="pWithBreakBefore" select="$paragraph/preceding-sibling::w:p[w:pPr/w:pageBreakBefore]"/>
	
	<!--Tengo que tener en cuenta 3 cosas para saber cuantos saltos de páginas hay antes del párrafo actual
		pasado como parámetro:
			1-	Los tags br. Estos directamente los cuento a todos.
			2-	Los tags pageBreakBefore. Estos debo contarlo solamente si en el párrafo anterior no hay un
				br.
			3-	Un pageBreakBefore en el párrafo actual. Este obviamente debo contarlo también, ya que me 
				está indicando que antes del párrafo actual hay un salto, pero solamente debo hacerlo si
				en el párrafo anterior no hay un br.-->
	<xsl:value-of select="count($pWithBr) +
						  count($pWithBreakBefore[not(preceding-sibling::w:p[1]/w:r/w:br[@w:type = 'page'])]) +
						  count($paragraph[w:pPr/w:pageBreakBefore and not(preceding-sibling::w:p[1]/w:r/w:br[@w:type = 'page'])])"/>
</xsl:template>

<!--***********************************************************************************************
	Cuenta la cantidad de títulos que hay antes de cierto párrafo.

	paragraph:	el elemento 'p' desde el cual empezar a contar hacia atrás los títulos.

	Retorna el número de títulos antes del elemento 'paragraph' pasado como parámetro.
	***********************************************************************************************-->
<xsl:template name="countHeadingsBefore">
	<xsl:param name="paragraph"/>

	<xsl:value-of select="count(preceding-sibling::w:p/w:pPr/w:pStyle[@w:val = $headings])"/>
</xsl:template>

</xsl:stylesheet>