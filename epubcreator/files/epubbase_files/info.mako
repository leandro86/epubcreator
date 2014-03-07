<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title></title>
    <link href="../Styles/style.css" rel="stylesheet" type="text/css" />
</head><!-- rellenar los datos de la info que se consideren necesarios y borrar el resto -->

<body>
    <div class="info">
        % if originalTitle:
              <p>Título original: <em>${originalTitle}</em></p>
        % endif

        ## "author" (al igual que "translator" e "ilustrator") puede contener una 
        ## lista de autores concatenados con un ampersand, por lo que necesito 
        ## escaparlo con "| h"
        <p>${author if author else "Autor" | h}${", {0}".format(publicationYear) if publicationYear else ""}</p>

        % if translator:
              <p>Traducción: ${translator | h}</p>
        % endif

        % if ilustrator:
              <p>Ilustraciones: ${ilustrator | h}</p>
        % endif

        % if coverDesigner:
              <p>${coverDesignOrTweak} de cubierta: ${coverDesigner}</p><!-- usar «Diseño» si la cubierta fue creada especialmente para esta edición; «Retoque» si es una adaptación de otra existente -->
        % endif

        <p class="salto10">Editor digital: ${editor}</p><!--<p>Primer editor: Editor1 (r1.0 a 1.x)</p>-->
        <!--<p>Segundo editor: Editor2 (r2.0 a 2.x)</p>-->
        <!--<p>Tercer editor: Editor3 (r3.0 a 3.x)</p>-->
        <!--<p>Corrección de erratas: ColaboradorA, ColaboradorB y ColaboradorC</p>-->

        <p>ePub base r1.1</p>
    </div>

    <div class="vineta"><img alt="" height="20%" src="../Images/ex_libris.png" /></div>
</body>
</html>
