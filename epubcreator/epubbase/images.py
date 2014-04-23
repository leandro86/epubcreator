import imghdr

from PyQt4 import QtGui, QtCore


class CoverImage:
    WIDTH = 600
    HEIGHT = 900
    MAX_SIZE_IN_BYTES = 300 * 1000

    # Contiene los formatos de imágenes soportados. El primer elemento de cada tupla
    # indica el formato, y el segundo si es necesario realizarle un preprocesamiento para
    # abrirlo (toda imagen que no sea jpg debe ser convertida a jpg, lo que significa que
    # allowProcessing debe ser True).
    SUPPORTED_FORMATS = (("jpg", False), ("jpeg", False), ("bmp", True), ("png", True))

    # Formatos de imágenes que no necesitan ser preprocesados (es decir, allowProcessing puede
    # ser False: solo para los formatos jpg y jpeg).
    _SAFE_FORMATS = tuple([f[0] for f in SUPPORTED_FORMATS if not f[1]])

    def __init__(self, image, allowProcessing=True):
        """
        Clase para procesar la imagen de cubierta, redimensionarla según las medidas que
        indica el epub base, insertarle el logo, etc.

        @param image: un string con el path de la imagen, o los bytes de la misma.
        @param allowProcessing: indica si se permite modificar la imagen. De no permitirse, entonces
                                no puede aplicársele ningún tipo de procesamiento, lo que significa
                                que solo se va a admitir como formato de la imagen a abrir un jpg.

        @raise MaxSizeExceededError: cuando la imagen supera el tamaño máximo permitido, y solo cuando
                                     allowProcessing es False.
        @raise InvalidDimensionsError: cuando la imagen no tiene las dimensiones requeridas, y solo cuando
                                       allowProcessing es False.
        """
        if isinstance(image, str):
            with open(image, "rb") as f:
                self._originalImageBytes = f.read()
        else:
            self._originalImageBytes = image

        imageFormat = imghdr.what("", h=self._originalImageBytes)
        if imageFormat not in CoverImage._SAFE_FORMATS and not allowProcessing:
            raise ValueError("Debe permitirse el preprocesamiento para abrir una imagen de tipo '{0}'.".format(imageFormat))

        self._image = QtGui.QImage.fromData(self._originalImageBytes)
        self._allowProcessing = allowProcessing

        if not self._allowProcessing and len(self._originalImageBytes) > CoverImage.MAX_SIZE_IN_BYTES:
            raise MaxSizeExceededError()

        if self._image.width() != CoverImage.WIDTH or self._image.height() != CoverImage.HEIGHT:
            if self._allowProcessing:
                self._scale()
            else:
                raise InvalidDimensionsError()

    def toBytes(self):
        if self._allowProcessing:
            quality = self._findBestQuality()
            buffer = QtCore.QBuffer()
            self._image.save(buffer, "JPG", quality)
            return buffer.data()
        else:
            return self._originalImageBytes

    def _scale(self):
        self._image = self._image.scaled(CoverImage.WIDTH, CoverImage.HEIGHT, QtCore.Qt.IgnoreAspectRatio)

    def _compress(self, quality):
        buffer = QtCore.QBuffer()
        self._image.save(buffer, "JPG", quality)
        self._image = QtGui.QImage.fromData(buffer.data().data())

    def _findBestQuality(self):
        for quality in range(100, -1, -1):
            buffer = QtCore.QBuffer()
            self._image.save(buffer, "JPG", quality)

            if len(buffer.data().data()) <= CoverImage.MAX_SIZE_IN_BYTES:
                return quality

        raise Exception("Esto no debería pasar: no se encontró un nivel de compresión en el rango 0-100 capaz de reducir "
                        "lo suficiente el tamaño de la imagen.")


class InvalidDimensionsError(Exception):
    pass


class MaxSizeExceededError(Exception):
    pass