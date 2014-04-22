import imghdr

from PyQt4 import QtGui, QtCore


class CoverImage:
    WIDTH = 600
    HEIGHT = 900
    MAX_SIZE_IN_KB = 300

    # Contiene los formatos de imágenes soportados. El primer elemento de cada tupla
    # indica el formato, y el segundo si es necesario realizarle un preprocesamiento para
    # abrirlo (toda imagen que no sea jpg debe ser convertida a jpg, lo que significa que
    # allowProcessing debe ser True).
    SUPPORTED_FORMATS = (("jpg", False), ("jpeg", False), ("bmp", True), ("png", True))

    # Formatos de imágenes que no necesitan ser preprocesados (es decir, allowProcessing puede
    # ser False: solo para los formatos jpg y jpeg).
    _SAFE_FORMATS = tuple([f[0] for f in SUPPORTED_FORMATS if not f[1]])

    def __init__(self, image, allowProcessing=True):
        if isinstance(image, str):
            with open(image, "rb") as f:
                self._originalImageBytes = f.read()
        else:
            self._originalImageBytes = image

        imageFormat = imghdr.what("", h=self._originalImageBytes)
        if imageFormat not in CoverImage._SAFE_FORMATS and not allowProcessing:
            raise Exception("Debe permitirse el preprocesamiento para abrir una imagen de tipo '{0}'.".format(imageFormat))

        self._image = QtGui.QImage.fromData(self._originalImageBytes)
        self._allowProcessing = allowProcessing

        if not self._allowProcessing and len(self._originalImageBytes) / 1000 > CoverImage.MAX_SIZE_IN_KB:
            raise MaxSizeExceededError()

        if self._image.width() != CoverImage.WIDTH or self._image.height() != CoverImage.HEIGHT:
            if self._allowProcessing:
                self._scale()
            else:
                raise InvalidDimensionsError()

    def toBytes(self):
        if self._allowProcessing:
            buffer = QtCore.QBuffer()
            self._image.save(buffer, "JPG")
            return buffer.data()
        else:
            return self._originalImageBytes

    def _scale(self):
        self._image = self._image.scaled(CoverImage.WIDTH, CoverImage.HEIGHT, QtCore.Qt.IgnoreAspectRatio)


class InvalidDimensionsError(Exception):
    pass


class MaxSizeExceededError(Exception):
    pass