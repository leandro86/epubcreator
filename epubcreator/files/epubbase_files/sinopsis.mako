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
        <% paragraphs = synopsis.splitlines() %>        
        <p class="salto10">${paragraphs[0]}</p>
        % for p in paragraphs[1:]:
            % if p.startswith("<p"):
                  ${p}
            % else:
                  <p>${p}</p>
            % endif
        % endfor
    </div>
</body>
</html>
