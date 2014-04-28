import imghdr

from PyQt4 import QtGui, QtCore

from epubcreator.epubbase import names


class CoverImage:
    WIDTH = 600
    HEIGHT = 900
    MAX_SIZE_IN_BYTES = 300 * 1000

    WHITE_LOGO = 0
    BLACK_LOGO = 1
    GLOW_LOGO = 2
    NO_LOGO = 3

    # Contiene los formatos de imágenes soportados. El primer elemento de cada tupla
    # indica el formato, y el segundo si es necesario realizarle un preprocesamiento para
    # abrirlo (toda imagen que no sea jpg debe ser convertida a jpg, lo que significa que
    # allowProcessing debe ser True).
    SUPPORTED_FORMATS = (("jpg", False), ("jpeg", False), ("bmp", True), ("png", True))

    # Formatos de imágenes que no necesitan ser preprocesados (es decir, allowProcessing puede
    # ser False: solo para los formatos jpg y jpeg).
    _SAFE_FORMATS = tuple([f[0] for f in SUPPORTED_FORMATS if not f[1]])

    # Las cubiertas transparentes solamente con los logos.
    _LOGOS = {}

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
                imageBytes = f.read()
        else:
            imageBytes = image

        imageFormat = imghdr.what("", h=imageBytes)
        if imageFormat not in CoverImage._SAFE_FORMATS and not allowProcessing:
            raise ValueError("Debe permitirse el preprocesamiento para abrir una imagen de tipo '{0}'.".format(imageFormat))

        self._image = QtGui.QImage.fromData(imageBytes)
        self._allowProcessing = allowProcessing

        if not self._allowProcessing and len(imageBytes) > CoverImage.MAX_SIZE_IN_BYTES:
            raise MaxSizeExceededError()

        if self._image.width() != CoverImage.WIDTH or self._image.height() != CoverImage.HEIGHT:
            if self._allowProcessing:
                self._image = self._image.scaled(CoverImage.WIDTH, CoverImage.HEIGHT, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
                self._originalImageBytes = self._getImageBytes()
            else:
                raise InvalidDimensionsError()
        else:
            self._originalImageBytes = imageBytes

        self._quality = 100
        self._logo = CoverImage.NO_LOGO

    def compress(self, quality):
        if not self._allowProcessing:
            raise ValueError("Debe permitirse el procesamiento de la imagen para poder comprimirla.")

        self._quality = quality

    def size(self):
        return len(self._getImageBytes(self.quality()))

    def quality(self):
        return self._quality

    def insertLogo(self, logo):
        """
        Inserta un logo de epublibre en la imagen.

        @param logo: uno de estos posibles valores: WHITE_LOGO, BLACK_LOGO, GLOW_LOGO.
        """
        if not self._allowProcessing:
            raise ValueError("Debe permitirse el procesamiento de la imagen para poder insertarle un logo.")

        if not CoverImage._LOGOS:
            self._loadLogos()

        self._image = QtGui.QImage.fromData(self._originalImageBytes)

        # Ojo, al recargar la imagen, ahora la calidad vuelve a ser 100!
        self._quality = 100

        logoImage = CoverImage._LOGOS[logo]
        painter = QtGui.QPainter(self._image)
        painter.drawImage(0, 0, logoImage)
        painter.end()

        self._logo = logo

    def logo(self):
        return self._logo

    def toBytes(self, compressIfNecessary=True):
        """
        Retorna los bytes de la imagen.

        @param compressIfNecessary: indica si la imagen debe comprimirse (usando la mejor calidad posible) en
                                    caso de que el tamaño exceda el máximo permitido. Cuidado que un False acá
                                    significa que la imagen puede exceder el tamaño máximo permitido. Usar False
                                    cuando no se pretende guardar la imagen a disco, sino que solo se quiere
                                    previsualizarla.
        """
        if self._allowProcessing:
            if compressIfNecessary and self.size() > CoverImage.MAX_SIZE_IN_BYTES:
                self._quality = self._findBestQuality()
            return self._getImageBytes(self.quality())
        else:
            return self._originalImageBytes

    def clone(self):
        coverImage = CoverImage(self._originalImageBytes, self._allowProcessing)

        if self._allowProcessing:
            if self.logo() != CoverImage.NO_LOGO:
                coverImage.insertLogo(self.logo())

            if self.quality() != 100:
                coverImage.compress(self.quality())

        return coverImage

    def _getImageBytes(self, quality=100):
        if self._allowProcessing:
            buffer = QtCore.QBuffer()
            self._image.save(buffer, "JPG", quality)
            return buffer.data().data()
        else:
            return self._originalImageBytes

    def _findBestQuality(self):
        for quality in range(100, -1, -1):
            imageBytes = self._getImageBytes(quality)

            if len(imageBytes) <= CoverImage.MAX_SIZE_IN_BYTES:
                return quality

        raise Exception("Esto no debería pasar: no se encontró un nivel de compresión en el rango 0-100 capaz de reducir "
                        "lo suficiente el tamaño de la imagen.")

    def _loadLogos(self):
        CoverImage._LOGOS[CoverImage.WHITE_LOGO] = QtGui.QImage(names.getFullPathToFile(names.WHITE_LOGO_FOR_COVER))
        CoverImage._LOGOS[CoverImage.BLACK_LOGO] = QtGui.QImage(names.getFullPathToFile(names.BLACK_LOGO_FOR_COVER))
        CoverImage._LOGOS[CoverImage.GLOW_LOGO] = QtGui.QImage(names.getFullPathToFile(names.GLOW_LOGO_FOR_COVER))


class InvalidDimensionsError(Exception):
    pass


class MaxSizeExceededError(Exception):
    pass