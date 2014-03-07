<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title></title>
    <link href="../Styles/style.css" rel="stylesheet" type="text/css" />
</head><!-- este documento es opcional, debe eliminarse de ser innecesario -->

<body>
    <div class="dedicatoria">
        % if dedication:
              <% paragraphs = dedication.splitlines() %>
              % for p in paragraphs:
                    <p>${p}</p>
              % endfor
        % else:
              <p>Suspiró entonces mío Cid, de pesadumbre cargado, y comenzó a hablar así, justamente mesurado: «¡Loado seas, Señor, Padre que estás en lo alto! Todo esto me han urdido mis enemigos malvados».</p>

              <p class="salto05">A<small>NÓNIMO</small></p>
        % endif
    </div>
</body>
</html>
