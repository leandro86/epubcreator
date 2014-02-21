from misc import utils


class AbstractTransformer:
    """
    Clase abstracta para obtener los archivos, títulos y metadatos de algún documento de origen.
    Cuando se quiera procesar algún tipo de documento nuevo, debe crearse una clase derivada de ésta y
    sobreescribir obligatoriamente el método "transform", y opcionalmente el método "getMetadata".
    """

    def transform(self):
        """
        Obtiene los archivos y títulos de algún documento de origen.

        @return: un tupla de tres elementos que contiene: una lista de File, una lista de Title, y una lista de
                 TransformerLogMessage, con los mensajes de error o advertencias producidos.
                 Por convención, la lista de File contiene primero las imágenes y demás archivos, y luego
                 vienen todos los htmls, en el orden en el cual deben ser insertados en el epub.
        """
        raise NotImplemented

    def getMetadata(self):
        """
        Obtiene los metadatos del documento de origen.

        @return: un objeto Metadata.
        """
        raise NotImplemented


class TransformerLogMessage:
    MSG_TYPE = utils.Utilities.enum(WARNING=1, ERROR=2)

    def __init__(self, msgType, message):
        self.msgType = msgType
        self.message = message