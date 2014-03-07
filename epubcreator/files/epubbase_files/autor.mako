<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title></title>
    <link href="../Styles/style.css" rel="stylesheet" type="text/css" />
</head><!-- este documento es opcional, debe eliminarse de ser innecesario junto con el documento autor.jpg de la carpeta de imágenes -->

<body>
    <h1 class="oculto" title="Autor"></h1><!-- puede cambiarse a «Autora» o «Autores» de ser necesario -->

    <div class="vineta"><img alt="" height="40%" src="../Images/autor.jpg" /></div><!-- atención: por compatibilidad, este archivo de imagen no debe exceder los 600px de ancho ni haber sido guardado como jpeg «progresivo» -->

    <div class="autor">
        % if authorBiography:
              <% paragraphs = authorBiography.splitlines() %>
              % for p in paragraphs:
                    <p>${p}</p>
              % endfor
        % else:
              <p>N<small>OMBRE DEL</small> A<small>UTOR</small> (Reikiavik, Islandia, 2013 - Terra III, 3096). Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc vel libero sed est ultrices elementum at vel lacus. Sed laoreet, velit nec congue pellentesque, quam urna pretium nunc, et ultrices nulla lacus non libero.</p>

              <p>Integer eu leo justo, vel sodales arcu. Donec posuere nunc in lectus laoreet a rhoncus enim fermentum. Nunc luctus accumsan ligula eu molestie.</p>
        % endif
    </div>
</body>
</html>
