<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title></title>
    <link href="../Styles/style.css" rel="stylesheet" type="text/css" />
</head>

<body>
    <div class="sinopsis">        
        % if synopsis:
              <% paragraphs = synopsis.splitlines() %>        
              <p class="salto10">${paragraphs[0]}</p>
              % for p in paragraphs[1:]:
                    <p>${p}</p>
              % endfor
        % else:
              <p class="salto10">Yo por bien tengo que cosas tan señaladas, y por ventura nunca oídas ni vistas, vengan a noticia de muchos y no se entierren en la sepultura del olvido, pues podría ser que alguno que las lea halle algo que le agrade, y a los que no ahondaren tanto los deleite.</p>

              <p>Y a este propósito dice Plinio que no hay libro, por malo que sea, que no tenga alguna cosa buena; mayormente que los gustos no son todos unos, mas lo que uno no come, otro se pierde por ello. <span class="nosep">L<small>ÁZARO</small></span> <small>DE</small> <span class="nosep">T<small>ORMES</small>.</span></p>
        % endif
    </div>
</body>
</html>
