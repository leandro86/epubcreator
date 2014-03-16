import unicodedata


def removeSpecialCharacters(s):
    """
    Elimina acentos y caracteres no latinos de un string.

    @param s: el string del cual eliminar los caracteres.

    @return: un string con los caracteres eliminados.
    """
    return unicodedata.normalize("NFKD", s).encode('ASCII', 'ignore').decode()