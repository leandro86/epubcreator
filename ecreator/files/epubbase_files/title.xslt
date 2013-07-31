<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
				xmlns:str="http://exslt.org/strings"
				xmlns:date="http://exslt.org/dates-and-times" 
				extension-element-prefixes="str date"
				version="1.0">

<xsl:output method="xml" 
			doctype-public="-//W3C//DTD XHTML 1.1//EN"
			doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd" 
			standalone="no" 
			encoding="utf-8" 
			omit-xml-declaration="no" 
			indent="yes" 
			version="1.0"/>

<xsl:param name="author">Autor</xsl:param>
<xsl:param name="title">Título</xsl:param>
<xsl:param name="subtitle"></xsl:param>
<xsl:param name="editor">Editor</xsl:param>

<xsl:template match="/">
	<html xmlns="http://www.w3.org/1999/xhtml">
		<head>
		  <title></title>
		  <link href="../Styles/style.css" rel="stylesheet" type="text/css" />
		</head>
		
		<body>
			<p class="tlogo"><span><img alt="" src="../Images/EPL_logo.png" width="100%" /></span></p>				
			<p class="tautor"><code class="sans"><xsl:value-of select="$author"/></code></p>
			<h1 class="ttitulo"><strong class="sans"><xsl:value-of select="$title"/></strong></h1>
			
			<xsl:if test="$subtitle">
				<p class="tsubtitulo"><strong class="sans"><xsl:value-of select="$subtitle"/></strong></p>
				<xsl:comment> esta línea es opcional, debe eliminarse si no tiene texto </xsl:comment>
			</xsl:if>
			
			<p class="trevision"><strong class="sans">ePub r1.0</strong></p>		
			<p class="tfirma">
				<strong class="sans"><xsl:value-of select="$editor"/></strong>
				<xsl:text> </xsl:text>

				<xsl:variable name="day"><xsl:call-template name="currentDay"/></xsl:variable>
				<xsl:variable name="month"><xsl:call-template name="currentMonth"/></xsl:variable>
				<xsl:variable name="year"><xsl:call-template name="currentYear"/></xsl:variable>
									
				<code class="tfecha sans"><xsl:value-of select="concat($day, '.', $month, '.', $year)"/></code>
			</p>
		</body>
	</html>
</xsl:template>

<!--***********************************************************************************************
	Padea un string con ceros a la izquierda.

	string:	el string a paddear.
	maxLen:	el tamaño máximo del string resultante. Ej: el string '7', con maxLen 
			de 3, retorna: '007'.

	Retorna el string padeado.
	***********************************************************************************************-->
<xsl:template name="padZeroLeft">
	<xsl:param name="string"/>
	<xsl:param name="maxLen"/>
	
	<xsl:variable name="zeros">
		<xsl:value-of select="str:padding($maxLen - string-length($string), '0')"></xsl:value-of>
	</xsl:variable>
	
	<xsl:value-of select="concat($zeros, $string)"></xsl:value-of>
</xsl:template>

<!--***********************************************************************************************
	Retorna el día actual, en dos dígitos.
	***********************************************************************************************-->
<xsl:template name="currentDay">
	<xsl:call-template name="padZeroLeft">
		<xsl:with-param name="string" select="date:day-in-month()"/>
		<xsl:with-param name="maxLen" select="2"/>
	</xsl:call-template>
</xsl:template>

<!--***********************************************************************************************
	Retorna el mes actual, en dos dígitos.
	***********************************************************************************************-->
<xsl:template name="currentMonth">
	<xsl:call-template name="padZeroLeft">
		<xsl:with-param name="string" select="date:month-in-year()"/>
		<xsl:with-param name="maxLen" select="2"/>
	</xsl:call-template>
</xsl:template>

<!--***********************************************************************************************
	Retorna el año actual, en dos dígitos.
	***********************************************************************************************-->
<xsl:template name="currentYear">
	<xsl:value-of select="substring(date:year(), 3, 2)"/>
</xsl:template>

</xsl:stylesheet>