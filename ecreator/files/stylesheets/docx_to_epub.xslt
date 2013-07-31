<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet	xmlns="http://www.w3.org/1999/xhtml"
				xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
				xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" 
				xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" 			
				exclude-result-prefixes="w wp" 
				version="1.0">

<xsl:output method="xml" 
			doctype-public="-//W3C//DTD XHTML 1.1//EN"
			doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd" 
			standalone="no" 
			encoding="utf-8" 
			omit-xml-declaration="no" 
			indent="yes" 
			version="1.0"/>

<!--El path hacia el archivo footnotes.xml-->
<xsl:param name="footNotesXmlPath">footnotes_path</xsl:param>

<!--El path hacia el archivo styles.xml-->
<xsl:param name="stylesXmlPath">styles_path</xsl:param>

<!--Indica si deben ignorarse ("Y") o no ("N") los párrafos en blanco.
	En caso de "N", los párrafos en blanco se convierten a las clases del
	epub "salto10" o "salto25", según las siguientes reglas:
		Un párrafo en blanco:			"salto10"
		Dos o más párrafos en blanco:	"salto25"-->
<xsl:param name="ignoreEmptyParagraphs">Y</xsl:param>

<!--Necesito estas dos variables para poder comparar strings case-insensitive-->
<xsl:variable name="lowercase" select="'abcdefghijklmnopqrstuvwxyz'"/>
<xsl:variable name="uppercase" select="'ABCDEFGHIJKLMNOPQRSTUVWXYZ'"/>

<xsl:variable name="footNotesDoc" select="document($footNotesXmlPath)"/>
<xsl:variable name="stylesDoc" select="document($stylesXmlPath)"/>

<!--Una cosa es el id del estilo, y otra el nombre. En document.xml, se utiliza el id del estilo para referenciarlo.
	Cada estilo está especificado en styles.xml: su id, nombre, formato, estilo padre, etc. Necesito hacer
	un mapeo entre el id del estilo y su nombre.
	Como se ve, en ningún momento hago referencia styles.xml, eso es porque <xslt:key> no me permite 
	usar la función "document" ni variables tampoco. Por eso es que al momento de buscar un valor con la 
	función key(), necesito previamente	cambiar el contexto hacia styles.xml, utilizando un for-each.-->
<xsl:key name="styles" match="w:styles/w:style/w:name/@w:val" use="parent::w:name/parent::w:style/@w:styleId"></xsl:key>

<!--Necesito tener una referencia al documento principal para poder leer del mismo cuando
	me encuentro en otro contexto, por ejemplo, analizando el contenido de las notas en footnotes.xml-->
<xsl:variable name="mainDocument" select="/"></xsl:variable>
			
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
			<xsl:if test="$footNotesDoc/w:footnotes">
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
	<!--En el archivo footnotes.xml cada nota al pie tiene un atributo id que las identifica, comenzando
		con el valor 1, e incrementándose secuencialmente. Esto me permite a mí insertar el número de nota
		al pie de forma sencilla.
		TODO: ¿esto es realmente así siempre? ¿Habrá algún caso donde en el docx los ids se 
		numeren de otra forma? De ser así, debo modificar todoo esto.-->
	<xsl:variable name="noteNumber" select="parent::w:footnote/@w:id"/>

	<p>
		<!--Si es el primer párrafo, debo insertar el id de la nota-->
		<xsl:if test="not(preceding-sibling::w:p)">
			<a id="nota{$noteNumber}"></a>
			<sup>
				<xsl:text>[</xsl:text>
				<xsl:value-of select="$noteNumber"/>
				<xsl:text>]</xsl:text>
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
	Procesa los párrafos.
	***********************************************************************************************-->
<xsl:template match="w:p">
	<xsl:choose>
		<xsl:when test="descendant::w:t and normalize-space(.) != ''">
			<xsl:variable name="style">
				<xsl:variable name="currentStyleId" select="w:pPr/w:pStyle/@w:val"/>
				<!--Obtengo el nombre del estilo a partir del id, haciendo un cambio de contexto hacia
					styles.xml. (Ver arriba en la definición de "styles" por qué es necesario el
					cambio de contexto.)-->
				<xsl:for-each select="$stylesDoc">
					<xsl:value-of select="translate(key('styles', $currentStyleId), $uppercase, $lowercase)"/>
				</xsl:for-each>
			</xsl:variable>
					
			<!--Dependiendo de si el párrafo tiene un estilo de título aplicado o no, genero el
				tag "h" o "p".-->
			<xsl:variable name="tag">
				<xsl:choose>
					<!--El nombre del estilo ya fue convenientemente covertido a minúsculas...-->
					<xsl:when test="starts-with($style, 'encabezado') or starts-with($style, 'heading')">
						<xsl:value-of select="concat('h', substring($style, string-length($style), 1))"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of select="'p'"/>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:variable>
			
			<xsl:variable name="classValue">
				<xsl:if test="$ignoreEmptyParagraphs = 'N' and preceding-sibling::w:p[1][not(w:r/w:t[normalize-space(text()) != ''])]">
					<xsl:text>salto</xsl:text>						
					<xsl:choose>
						<xsl:when test="preceding-sibling::w:p[2][not(w:r/w:t[normalize-space(text()) != ''])]">25 </xsl:when>
						<xsl:otherwise>10 </xsl:otherwise>
					</xsl:choose>
				</xsl:if>
				<!--Si un párrafo es un heading, entonces ya tiene un estilo asignado, y según parece, un
					párrafo no puede tener más de un estilo simultáneamente: por eso pregunto que el tag
					no sea un heading.-->
				<xsl:if test="$tag != 'h' and starts-with($style, 'epub_')">
					<xsl:value-of select="substring($style, 6)"/>
				</xsl:if>
			</xsl:variable>

			<xsl:element name="{$tag}">
				<!--Solamente si el tag no es un encabezado es cuando debo comprobar por los estilos, ya
					que en el docx los títulos se especifican con estilos, y según parece, un párrafo no puede
					tener aplicado dos o más estilos simultáneamente.-->
				<xsl:if test="$classValue != ''">
					<xsl:attribute name="class"><xsl:value-of select="$classValue"/></xsl:attribute>									
				</xsl:if>
				<xsl:apply-templates/>
			</xsl:element>	
		</xsl:when>
		<xsl:when test="descendant::w:drawing">
			<p class="ilustra"><xsl:apply-templates/></p>
		</xsl:when>
	</xsl:choose>
	
	<xsl:call-template name="checkForSectionBreak"/>
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
<xsl:template match="w:drawing">
	<!--Los archivos de imágenes parecen estar nombrados siempre "image1.png", "image2.png", etc., en
		word y en libreoffice. Ahora, los ids usados en w:drawing difieren: en word empiezan a numerar
		desde 1, y en libreoffice desde 0. Por ahora la única solución que encontré para poner
		correctamente el id de la imagen es contar simplemente la cantidad de imágenes previas que
		hay. De esta manera no tengo que alterar al menos los nombres de las imágenes, y puedo
		guardarlas en el epub directamente tal cual están.
		Necesito contar primero las imágenes que pueden encontrarse en el mismo párrafo, pero en 
		runs anteriores. También debo contar las que se encuentran en párrafos anteriores.-->
	<xsl:variable name="imgId" select="count(parent::w:r/preceding-sibling::w:r/w:drawing) +
									   count(ancestor::w:p/preceding-sibling::w:p/w:r/w:drawing) + 1"/>
	<img src="../Images/image{$imgId}.png" alt=""></img>
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
	NOTA: está función debe ser llamada desde dentro de un 'p' (el context node debe ser un 'p').
	***********************************************************************************************-->
<xsl:template name="checkForSectionBreak">
	<xsl:if test="w:r[w:br/@w:type = 'page'] or following-sibling::w:p[1]/w:pPr/w:pageBreakBefore">
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

</xsl:stylesheet>
