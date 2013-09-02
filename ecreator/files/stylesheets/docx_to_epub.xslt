<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet	xmlns="http://www.w3.org/1999/xhtml"
				xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
				xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" 
				xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
				xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"
				xmlns:rels="http://schemas.openxmlformats.org/package/2006/relationships"
				xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"				
				xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
				xmlns:v="urn:schemas-microsoft-com:vml"
				exclude-result-prefixes="w a pic rels r mc v" 
				version="1.0">

<xsl:import href="common.xslt"/>

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

<!--Llevar un contador de notas implicaría otro overhead más, además de que no es necesario porque en el propio footnotes.xml
	se indica con un atributo "id" el número de nota. El problema es que este "id" no siempre empieza a contar desde 1, a veces
	lo hace desde 2 (y podría hacerlo desde cualquier otro número, aunque esto no lo he visto por ahora). Esto no es
	un problema grave, porque al fin y al cabo los ids no interesan, pero no es muy estético que digamos. Para solucionar esto
	hago un pequeño cálculo sobre el id de la primer nota, de manera de obtener una especie de delfa u offset, que me va a 
	indicar el valor que tengo que restarle a los subsecuentes id's de notas que me encuentre para corregirlo, y así siempre
	en el epub resultante los ids de notas empiezan a contar desde 1.
	Ojo que supongo que los ids en footnotes.xml son consecutivos, si llegara a darse el caso de un docx que no es así, no me queda
	otra que llevar un contador de notas propio.-->
<xsl:variable name="noteIdDelta">
	<xsl:variable name="firstId" select="$footNotesDoc/w:footnotes/w:footnote[not(@w:type)][1]/@w:id"/>
	<xsl:choose>
		<xsl:when test="$firstId != 1">	<xsl:value-of select="$firstId - ($firstId - 1)"/></xsl:when>
		<xsl:otherwise>0</xsl:otherwise>
	</xsl:choose>
</xsl:variable>

<!--***********************************************************************************************	
	Warnings.
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
				<xsl:apply-templates select="w:body//w:footnoteReference" mode="content"/>
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
	<xsl:variable name="nodeId" select="parent::w:footnote/@w:id"/>
	<xsl:variable name="noteNumber" select="$nodeId - $noteIdDelta"/>

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
					<xsl:with-param name="node" select="$mainDocument/w:document/w:body/*[descendant::w:r/w:footnoteReference[@w:id = $nodeId]]"/>
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
				<xsl:with-param name="noteId" select="concat('nota', $noteNumber, 'ref')"/>
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
	<xsl:variable name="styleId" select="w:pPr/w:pStyle/@w:val"/>
	<xsl:variable name="styleName">
		<xsl:call-template name="getStyleName">
			<xsl:with-param name="styleId" select="$styleId"/>
		</xsl:call-template>
	</xsl:variable>

	<xsl:choose>		
		<xsl:when test="starts-with($styleName, 'Encabezado') or starts-with($styleName, 'heading')">	
			<xsl:call-template name="processHeading">
				<xsl:with-param name="styleName" select="$styleName"/>
			</xsl:call-template>
		</xsl:when>
		<xsl:otherwise>
			<xsl:call-template name="processParagraph">
				<xsl:with-param name="styleId" select="$styleId"/>
				<xsl:with-param name="styleName" select="$styleName"/>
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

	styleName: el nombre del estilo aplicado al párrafo actual.
	***********************************************************************************************-->
<xsl:template name="processHeading">
	<xsl:param name="styleName"/>
	
	<xsl:variable name="headingNumber"><xsl:value-of select="substring($styleName, string-length($styleName), 1)"/></xsl:variable>
	<xsl:choose>
		<!--Si el número de heading es mayor a 6, no lo proceso como heading, sino como párrafo común.-->
		<xsl:when test="$headingNumber > 6">
			<xsl:call-template name="processParagraph">
				<xsl:with-param name="style" select="$styleName"/>
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

	styleId: el id del estilo aplicado al párrafo actual.
	styleName: el nombre del estilo aplicado al párrafo actual.
	***********************************************************************************************-->
<xsl:template name="processParagraph">
	<xsl:param name="styleId"/>
	<xsl:param name="styleName"/>

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
			<!--Me fijo si es necesario agregar la clase "salto", dependiendo de si debo procesar los párrafos en blanco y de cuántos
				párrafos en blanco hay antes del actual que estoy procesando.-->	
			<xsl:variable name="marginClass">		
				<xsl:if test="$ignoreEmptyParagraphs = 'N' and preceding-sibling::w:p[1][not(w:r/w:t[normalize-space(text()) != ''])]">
					<xsl:text>salto</xsl:text>						
					<xsl:choose>
						<xsl:when test="preceding-sibling::w:p[2][not(w:r/w:t[normalize-space(text()) != ''])]">25 </xsl:when>
						<xsl:otherwise>10 </xsl:otherwise>
					</xsl:choose>
				</xsl:if>
			</xsl:variable>
			<!--Compruebo si se trata de un estilo estándar que debo procesar, o de algún estilo customizado-->
			<xsl:variable name="classValue">
				<!--Es un estilo propio?-->
				<xsl:call-template name="parseCustomStyle">
					<xsl:with-param name="styleName" select="$styleName"/>
				</xsl:call-template>
			</xsl:variable>
			
			<!--Si dos o más parrafos consecutivos comparten el mismo estilo, entonces los agrupo en un div-->
			<xsl:variable name="divContainer">
				<!--Me fijo si el párrafo tiene aplicado un estilo que me interesa, es decir, alguno que proceso-->
				<xsl:if test="$styleId != '' and $classValue != ''">
					<xsl:variable name="previousParagraphStyleId"><xsl:value-of select="preceding-sibling::w:p[1]/w:pPr/w:pStyle/@w:val"/></xsl:variable>
					<xsl:variable name="nextParagraphStyleId"><xsl:value-of select="following-sibling::w:p[1]/w:pPr/w:pStyle/@w:val"/></xsl:variable>
					
					<xsl:choose>
						<!--Debo abrir el div?-->
						<xsl:when test="$styleId != $previousParagraphStyleId and $styleId = $nextParagraphStyleId">O</xsl:when>
						<xsl:when test="$styleId = $previousParagraphStyleId">
							<xsl:choose>
								<!--Está el párrafo actual dentro de un div que ya fue abierto anteriormente, y que
									todavía no debe ser cerrado, porque hay al menos otro párrafo más con el mismo estilo?-->
								<xsl:when test="$styleId = $nextParagraphStyleId">N</xsl:when>
								<!--Debo cerrar el div?-->
								<xsl:otherwise>C</xsl:otherwise>
							</xsl:choose>
						</xsl:when>
					</xsl:choose>							
				</xsl:if>
			</xsl:variable>
			
			<!--Abro el div de ser necesario, agregando la clase correspondiente-->
			<xsl:if test="$divContainer = 'O'">
				<xsl:text disable-output-escaping="yes">&lt;div class="</xsl:text>
				<xsl:value-of select="$classValue"/>
				<xsl:text disable-output-escaping="yes">"&gt;</xsl:text>
			</xsl:if>
						
			<xsl:element name="{$tag}">
				<!--Le asigno una clase al párrafo solo si se trata de la clase "salto", o si bien tiene asignado algún
					otro estilo, pero dicho párrafo no se encuentra dentro de un div-->
				<xsl:if test="$marginClass != '' or ($classValue != '' and $divContainer = '')">
					<xsl:attribute name="class">
						<xsl:if test="$marginClass != ''">
							<xsl:value-of select="$marginClass"/>
						</xsl:if>
						<xsl:if test="$classValue != '' and $divContainer = ''">
							<xsl:value-of select="$classValue"/>
						</xsl:if>
					</xsl:attribute>									
				</xsl:if>
				<xsl:apply-templates/>	
			</xsl:element>
			
			<!--Cierro el div, si es necesario-->
			<xsl:if test="$divContainer = 'C'">
				<xsl:text disable-output-escaping="yes">&lt;/div&gt;</xsl:text>						
			</xsl:if>
		</xsl:when>
		<xsl:when test="not(descendant::w:t) and (descendant::pic:pic[1] or descendant::w:pict[1])">
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
	<xsl:variable name="styleId" select="w:rPr/w:rStyle/@w:val"/>
	<xsl:variable name="styleName">
		<xsl:call-template name="getStyleName">
			<xsl:with-param name="styleId" select="$styleId"/>
		</xsl:call-template>
	</xsl:variable>
	
	<xsl:variable name="classValue">
		<xsl:if test="$styleName">
			<xsl:call-template name="parseCustomStyle">
				<xsl:with-param name="styleName" select="$styleName"/>
			</xsl:call-template>
		</xsl:if>
	</xsl:variable>
	
	<!--Es necesario utilizar un span si el run tiene algún estilo que me interesa procesar-->
	<xsl:variable name="spanContainer">
		<xsl:if test="$classValue != ''">
			<xsl:variable name="previousRunStyleId"><xsl:value-of select="preceding-sibling::w:r[1]/w:rPr/w:rStyle/@w:val"/></xsl:variable>
			<xsl:variable name="nextRunStyleId"><xsl:value-of select="following-sibling::w:r[1]/w:rPr/w:rStyle/@w:val"/></xsl:variable>	
			
			<!--Debo abrir el span?-->
			<xsl:if test="$styleId != $previousRunStyleId">
				<xsl:value-of select="'O'"/>
			</xsl:if>
			<!--Debo cerrar el span?-->
			<!--Notar que totalmente posible que sea necesario abrir un span en un run, y luego tener que
				cerrarlo en el mismo run.-->
			<xsl:if test="$styleId != $nextRunStyleId">
				<xsl:value-of select="'C'"/>
			</xsl:if>
		</xsl:if>
	</xsl:variable>
		
	<!--Abro el span de ser necesario, agregando la clase correspondiente-->
	<xsl:if test="contains($spanContainer, 'O')">
		<xsl:text disable-output-escaping="yes">&lt;span class="</xsl:text>
		<xsl:value-of select="$classValue"/>
		<xsl:text disable-output-escaping="yes">"&gt;</xsl:text>
	</xsl:if>

	<!--TODO: por ahora, esto lo dejo así. No encontré la forma todavía de poder abrir y cerrar los tags
		de formato de manera elegante. Es muy difícil hacerlo sin poder mantener algún tipo de estado, algo
		que me indique qué formatos siguen abierto de runs anteriores, así puedo cerrar todos los anidamientos
		de manera acorde. Me limité a copiar la solución que usó tarloth en su planilla, que reconstruye de
		manera elegante los tags en la mayoría de los casos (cuando el formato de los runs que se comparan es
		EXACTAMENTE el mismo)-->
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
	
	<!--Cierro el span, si es necesario-->
	<xsl:if test="contains($spanContainer, 'C')">
		<xsl:text disable-output-escaping="yes">&lt;/span&gt;</xsl:text>						
	</xsl:if>	
</xsl:template>

<!--***********************************************************************************************
	Procesa una referencia a una nota al pie.
	***********************************************************************************************-->
<xsl:template match="w:footnoteReference">
	<xsl:variable name="noteNumber" select="./@w:id - $noteIdDelta"/>
	<a id="nota{$noteNumber}ref" href="../Text/notas.xhtml#nota{$noteNumber}"><sup>[<xsl:value-of select="$noteNumber"/>]</sup></a>
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
	
	<xsl:call-template name="insertImage">
		<xsl:with-param name="name" select="$imageName"/>
	</xsl:call-template>
</xsl:template>

<!--***********************************************************************************************
	Procesa las imágenes, matcheando un tag para las imágenes ya en desuso, que se usaba en
	word 2007, pero que abby finereader parece utilizar al convertir a docx.
	***********************************************************************************************-->
<xsl:template match="w:pict">
	<xsl:variable name="rId">
		<xsl:value-of select="descendant::v:imagedata[1]/@r:id"/>	
	</xsl:variable>
	
	<xsl:if test="$rId != ''">
		<xsl:variable name="imageName">
			<xsl:value-of select="substring-after($relsDoc/rels:Relationships/rels:Relationship[@Id = $rId]/@Target, 'media/')"/>
		</xsl:variable>
			
		<xsl:call-template name="insertImage">
			<xsl:with-param name="name" select="$imageName"/>
		</xsl:call-template>
	</xsl:if>
	
	<!--Puede contener un textbox o un shape dentro, por lo que debo procesar texto si lo hay-->
	<xsl:apply-templates/>
</xsl:template>

<!--***********************************************************************************************
	Procesa los textboxes y shapes.
	***********************************************************************************************-->
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

	Retorna un string de 5 caracteres, donde un "-" significa ausencia de formato, y "*" significa
	que ese formato está aplicado al run. Los 5 caracteres representan, en orden:
		1-	Negrita
		2-	Itálica
		3-	Superíndice
		4-	Subíndice
		5-	Subrayado
	Ejemplo: "*-*-*", significa que el run tiene aplicado los formatos: negrita, superíndice y
					  subrayado.
	***********************************************************************************************-->	
<xsl:template name="transformRunFormats">
	<xsl:param name="run"/>	

	<xsl:choose>
		<xsl:when test="not($run[w:rPr])">
			<xsl:text>-----</xsl:text>
		</xsl:when>				
		<xsl:otherwise>
			<!--Obtengo los formatos aplicados al run-->
			<xsl:variable name="formats" select="$run/w:rPr"/>
			
			<!--Además de los formatos, un run puede tener aplicado un estilo. Dicho estilo también tiene
				varias propiedades, entre ellas, posiblemente un formato. Debo obtener también estos formatos
				que son propios al estilo, porque puede suceder que algún texto esté en negrita, pero no porque
				se le aplicó el formato negrita, sino porque tiene aplicado un estilo particular que entre sus
				propiedades tiene definido el formato negrita. Esto sucede a menudo cuando se realiza la conversión
				desde un pdf a docx utilizando abby finereader: no le aplica "formatos" al texto, sino que le aplica
				"estilos" propios.-->
			<xsl:variable name="style" select="$stylesDoc/w:styles/w:style[@w:styleId = $run/w:rPr/w:rStyle/@w:val]/w:rPr"/>
			
			<!--Negrita-->
			<xsl:choose>
				<xsl:when test="$formats/w:b or $style/w:b">*</xsl:when>
				<xsl:otherwise>-</xsl:otherwise>
			</xsl:choose>
			<!--Itálica-->
			<xsl:choose>
				<xsl:when test="$formats/w:i or $style/w:i">*</xsl:when>
				<xsl:otherwise>-</xsl:otherwise>
			</xsl:choose>
			<!--Superíndice-->
			<xsl:choose>
				<xsl:when test="$formats/w:vertAlign/@w:val='superscript'">*</xsl:when>
				<xsl:otherwise>-</xsl:otherwise>
			</xsl:choose>
			<!--Subíndice-->
			<xsl:choose>
				<xsl:when test="$formats/w:vertAlign/@w:val='subscript'">*</xsl:when>
				<xsl:otherwise>-</xsl:otherwise>
			</xsl:choose>
			<!--Subrayado-->
			<xsl:choose>
				<xsl:when test="$formats/w:u or $style/w:u">*</xsl:when>
				<xsl:otherwise>-</xsl:otherwise>
			</xsl:choose>
		</xsl:otherwise>
	</xsl:choose>
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
				<xsl:with-param name="node" select="."/>
			</xsl:call-template>
		</xsl:variable>
		
		<xsl:call-template name="startNewSection">
			<!--Sumo uno, porque al principio de todoo agregué ya agregué la section 0.-->
			<xsl:with-param name="number" select="$sectionsBeforeCount + 1"/>
		</xsl:call-template>
	</xsl:if>
</xsl:template>

<!--***********************************************************************************************
	Cuenta la cantidad de saltos de páginas anteriores a algún elemento. Ojo que solamente busco
	saltos de páginas en los siblings anteriores al "node" dado, no en sus ancestros y demás, por
	lo que es responsabilidad del caller llamar a esta función con el nodo adecuado.

	node:	el elemento del cual se van a examinar los siblings anteriores en busca de saltos de 
			página.

	Retorna el número de saltos de páginas que se encontraron.
	***********************************************************************************************-->
<xsl:template name="countSectionsBefore">
	<xsl:param name="node"/>
	
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
	<xsl:variable name="pWithBr" select="$node/preceding-sibling::w:p[w:r/w:br[@w:type = 'page']]"/>
	<xsl:variable name="pWithBreakBefore" select="$node/preceding-sibling::w:p[w:pPr/w:pageBreakBefore]"/>
	
	<!--Tengo que tener en cuenta 3 cosas para saber cuantos saltos de páginas hay antes del node actual
		pasado como parámetro:
			1-	Los tags br. Estos directamente los cuento a todos.
			2-	Los tags pageBreakBefore. Estos debo contarlo solamente si en el párrafo anterior no hay un
				br.
			3-	Un pageBreakBefore en el párrafo actual. Este obviamente debo contarlo también, ya que me 
				está indicando que antes del párrafo actual hay un salto, pero solamente debo hacerlo si
				en el párrafo anterior no hay un br.-->
	<xsl:value-of select="count($pWithBr) +
						  count($pWithBreakBefore[not(preceding-sibling::w:p[1]/w:r/w:br[@w:type = 'page'])]) +
						  count($node[w:pPr/w:pageBreakBefore and not(preceding-sibling::w:p[1]/w:r/w:br[@w:type = 'page'])])"/>
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

<!--***********************************************************************************************
	Retorna el nombre de un estilo asociado a un id.

	styleId: el id del estilo.
	***********************************************************************************************-->
<xsl:template name="getStyleName">
	<xsl:param name="styleId"/>

	<!--Obtengo el nombre del estilo a partir del id, haciendo un cambio de contexto hacia
		styles.xml (el cambio de contexto es necesario dada una limitación de xslt 1.0)-->
	<xsl:for-each select="$stylesDoc">
		<xsl:value-of select="key('styles', $styleId)"/>
	</xsl:for-each>
</xsl:template>

<!--***********************************************************************************************
	Comprueba si un estilo dado es un estilo creado por el usuario.

	styleName: el nombre del estilo a comprobar.

	Retorna el nombre del estilo, si es un estilo custom; sino vacío.
	***********************************************************************************************-->
<xsl:template name="parseCustomStyle">
	<xsl:param name="styleName"/>

	<xsl:if test="starts-with($styleName, 'epub_')">
		<xsl:value-of select="substring($styleName, 6)"/>
	</xsl:if>
</xsl:template>

</xsl:stylesheet>