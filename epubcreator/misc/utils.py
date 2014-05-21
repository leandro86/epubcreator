import unicodedata
import re
import difflib
import pprint

_controlChars = None


def removeSpecialCharacters(s):
    """
    Elimina acentos y caracteres no latinos de un string.

    @param s: el string del cual eliminar los caracteres.

    @return: un string con los caracteres eliminados.
    """
    return unicodedata.normalize("NFKD", s).encode('ASCII', 'ignore').decode()


def removeTags(s):
    """
    Elimina los tags de un string.

    @param s: el string del cual eliminar los tags.

    @return: un string con los tags eliminados.
    """
    return re.sub("<[^>]*>", "", s)


def assertXhtmlsAreEqual(xml1, xml2):
    # Elimina pretty-print.
    normal1 = re.sub(r"\r?\n\s*<", "<", xml1.decode()).strip()
    normal2 = re.sub(r"\r?\n\s*<", "<", xml2.decode()).strip()

    if normal1 != normal2:
        lines1 = re.sub(r"(</\w+>)", r"\1\n", normal1).splitlines()
        lines2 = re.sub(r"(</\w+>)", r"\1\n", normal2).splitlines()

        dif = [d for d in list(difflib.Differ().compare(lines1, lines2)) if d.startswith("+") or d.startswith("-")]

        raise AssertionError("Los xhtmls no son iguales:\n\n{0}".format(pprint.pformat(dif)))


def removeControlCharacters(s):
    """
    Elimina todos los caracteres de control de un string, exceptuando \t, \r y \n.
    """
    global _controlChars

    if _controlChars is None:
        chars = set(chr(c) for c in range(32))

        for c in ((chr(c) for c in (9, 10, 13))):
            chars.remove(c)

        _controlChars = re.compile("|".join(chars))

    return _controlChars.sub("", s)