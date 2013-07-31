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

<xsl:template match="/">
	<html xmlns="http://www.w3.org/1999/xhtml">
		<head>
		  <title></title>
		  <link href="../Styles/style.css" rel="stylesheet" type="text/css" />
		</head>
		
		<xsl:comment> no modificar esta página </xsl:comment><xsl:text>&#10;</xsl:text>
		<xsl:comment> atención: por problemas de compatibilidad con algunos dispositivos, EN NINGÚN CASO los archivos de imágenes deben exceder los 300k de tamaño </xsl:comment>
	
		<body class="sinmargen">
			<h1 class="cubierta" title="Cubierta"><img alt="" src="../Images/cover.jpg" /></h1>
		</body>
	</html>
</xsl:template>

</xsl:stylesheet>