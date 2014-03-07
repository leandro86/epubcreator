<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title></title>
    <link href="../Styles/style.css" rel="stylesheet" type="text/css" />
</head>

<%! import datetime %>

<body>   
    <p class="tlogo"><span><img alt="" src="../Images/EPL_logo.png" width="100%" /></span></p>

    <p class="tautor">${author if author else "Autor"}</p>

    <h1 class="ttitulo">${title if title else "Título"}</h1>

    % if subtitle:
          <p class="tsubtitulo">${subtitle}</p><!-- esta línea es opcional, debe eliminarse si no tiene texto -->
    % endif

    <p class="trevision">ePub r1.0</p>    

    <p class="tfirma">${editor if editor else "Editor"} <span class="tfecha">${datetime.datetime.now().strftime("%d.%m.%y")}</span></p>
</body>
</html>
