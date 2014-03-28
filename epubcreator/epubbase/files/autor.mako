<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title></title>
    <link href="../Styles/style.css" rel="stylesheet" type="text/css" />
</head><!-- este documento es opcional, debe eliminarse de ser innecesario junto con el documento autor.jpg de la carpeta de imágenes -->

<body>
    % if title:
          <h1 class="oculto" title="${title}"></h1><!-- puede cambiarse a «Autora» o «Autores» de ser necesario -->
    % endif

    <div class="vineta"><img alt="" height="40%" src="../Images/${imageName}" /></div><!-- atención: por compatibilidad, este archivo de imagen no debe exceder los 600px de ancho ni haber sido guardado como jpeg «progresivo» -->

    <div class="autor">
        <% paragraphs = authorBiography.splitlines() %>
         % for p in paragraphs:
             % if p.startswith("<p"):
                   ${p}
             % else:
                   <p>${p}</p>
             % endif
         % endfor
    </div>
</body>
</html>
