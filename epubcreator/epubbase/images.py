import io

from PIL import Image

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

    def __init__(self, file, allowProcessing=True):
        """
        Clase para procesar la imagen de cubierta, redimensionarla según las medidas que
        indica el epub base, insertarle el logo, etc.

        @param file: un string con el path de la imagen, o los bytes de la misma.
        @param allowProcessing: indica si se permite modificar la imagen. De no permitirse, entonces
                                no puede aplicársele ningún tipo de procesamiento, lo que significa
                                que solo se va a admitir como formato de la imagen a abrir un jpg.

        @raise MaxSizeExceededError: cuando la imagen supera el tamaño máximo permitido, y solo cuando
                                     allowProcessing es False.
        @raise InvalidDimensionsError: cuando la imagen no tiene las dimensiones requeridas, y solo cuando
                                       allowProcessing es False.
        """
        if isinstance(file, str):
            with open(file, "rb") as f:
                imageBytes = f.read()
        else:
            imageBytes = file

        # Contiene la imagen actual con el logo, si fue insertado.
        self._image = Image.open(io.BytesIO(imageBytes))

        if allowProcessing:
            if self._image.size != (CoverImage.WIDTH, CoverImage.HEIGHT):
                self._image = self._image.resize((CoverImage.WIDTH, CoverImage.HEIGHT), resample=Image.ANTIALIAS)
        else:
            if self._image.format.lower() not in CoverImage._SAFE_FORMATS:
                raise ValueError("Debe permitirse el preprocesamiento para abrir una imagen de tipo '{0}'.".format(self._image.format))

            if not allowProcessing and len(imageBytes) > CoverImage.MAX_SIZE_IN_BYTES:
                raise MaxSizeExceededError()

            if self._image.size != (CoverImage.WIDTH, CoverImage.HEIGHT):
                raise InvalidDimensionsError()

        self._quality = 100
        self._logo = CoverImage.NO_LOGO

        # Contiene la imagen original, inalterada, de manera tal de que cuando deba insertar un logo pueda
        # hacerlo sobre una imagen "limpia".
        self._originalImage = self._image

        # Contiene los bytes originales de la imagen. Los necesito para poder retornar la imagen intacta
        # cuando no se ha permitido el procesamiento de las imágenes.
        self._originalImageBytes = imageBytes

        self._allowProcessing = allowProcessing

    def setQuality(self, quality):
        if not self._allowProcessing:
            raise ValueError("Debe permitirse el procesamiento de la imagen para poder comprimirla.")

        self._quality = quality

    def size(self):
        return len(self._saveImage(self.quality()))

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

        self._image = self._originalImage.copy()

        # Ojo, al recargar la imagen, ahora la calidad vuelve a ser 100!
        self._quality = 100

        logoImage = CoverImage._LOGOS[logo]
        self._image.paste(logoImage, mask=logoImage)

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
            return self._saveImage(self.quality())
        else:
            return self._originalImageBytes

    def clone(self):
        coverImage = CoverImage(self._originalImageBytes, self._allowProcessing)

        if self._allowProcessing:
            if self.logo() != CoverImage.NO_LOGO:
                coverImage.insertLogo(self.logo())

            if self.quality() != 100:
                coverImage.setQuality(self.quality())

        return coverImage

    def _saveImage(self, quality=100):
        if self._allowProcessing:
            buffer = io.BytesIO()
            self._image.save(buffer, "JPEG", quality=quality, optimize=True)
            return buffer.getvalue()
        else:
            return self._originalImageBytes

    def _findBestQuality(self):
        for quality in range(100, -1, -1):
            imageBytes = self._saveImage(quality)

            if len(imageBytes) <= CoverImage.MAX_SIZE_IN_BYTES:
                return quality

        raise Exception("Esto no debería pasar: no se encontró un nivel de compresión en el rango 0-100 capaz de reducir "
                        "lo suficiente el tamaño de la imagen.")

    def _loadLogos(self):
        CoverImage._LOGOS[CoverImage.WHITE_LOGO] = Image.open(names.getFullPathToFile(names.WHITE_LOGO_FOR_COVER))
        CoverImage._LOGOS[CoverImage.BLACK_LOGO] = Image.open(names.getFullPathToFile(names.BLACK_LOGO_FOR_COVER))
        CoverImage._LOGOS[CoverImage.GLOW_LOGO] = Image.open(names.getFullPathToFile(names.GLOW_LOGO_FOR_COVER))


class InvalidDimensionsError(Exception):
    pass


class MaxSizeExceededError(Exception):
    pass