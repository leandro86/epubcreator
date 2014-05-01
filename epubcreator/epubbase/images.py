import io

from PIL import Image

from epubcreator.epubbase import files


class AbstractEpubBaseImage:
    """
    Clase base para procesar la imágenes de cubierta y autores.
    """

    # Deben ser sobreescritos en las clases derivadas.
    WIDTH = -1
    HEIGHT = -1
    MAX_SIZE_IN_BYTES = -1

    _FORMATS_NO_NEED_PROCESSING = ("jpg", "jpeg")
    _FORMATS_NEED_PROCESSING = ("png", "bmp")

    def __init__(self, file, allowProcessing=True):
        """
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

        self._image = Image.open(io.BytesIO(imageBytes))

        # Creo que jpg no soporta el modo "P": al menos cuando quiero guardar la imagen como jpg, me tira error.
        # La ayuda de pillow dice: P (8-bit pixels, mapped to any other mode using a color palette)
        # En dicho caso, convierto la imagen a modo "RGB".
        if self._image.mode == "P":
            self._image = self._image.convert("RGB")

        if allowProcessing:
            if self._image.size != (self.WIDTH, self.HEIGHT):
                self._image = self._image.resize((self.WIDTH, self.HEIGHT), resample=Image.ANTIALIAS)
        else:
            if self._image.format.lower() not in self._FORMATS_NO_NEED_PROCESSING:
                raise ValueError("Debe permitirse el preprocesamiento para abrir una imagen de tipo '{0}'.".format(self._image.format))

            if not allowProcessing and len(imageBytes) > self.MAX_SIZE_IN_BYTES:
                raise MaxSizeExceededError()

            if self._image.size != (self.WIDTH, self.HEIGHT):
                raise InvalidDimensionsError()

            if "progressive" in self._image.info:
                raise ProgressiveImageError()

        self._quality = 100

        # Contiene la imagen original, inalterada, en caso de que deba realizarle algún tipo de procesamiento que requiera una imagen "limpia".
        self._originalImage = self._image

        # Contiene los bytes originales de la imagen. Los necesito para poder retornar la imagen intacta
        # cuando no se ha permitido el procesamiento de las imágenes.
        self._originalImageBytes = imageBytes

        self._allowProcessing = allowProcessing

    @classmethod
    def allowedFormatsToOpen(cls, allowProcessing):
        return cls._FORMATS_NEED_PROCESSING + cls._FORMATS_NO_NEED_PROCESSING if allowProcessing else cls._FORMATS_NO_NEED_PROCESSING

    def setQuality(self, quality):
        if not self._allowProcessing:
            raise ValueError("Debe permitirse el procesamiento de la imagen para poder comprimirla.")

        self._quality = quality

    def size(self):
        if self._allowProcessing:
            return len(self._getBytes(self._image, self.quality()))
        else:
            return len(self._originalImageBytes)

    def quality(self):
        return self._quality

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
            if compressIfNecessary and self.size() > self.MAX_SIZE_IN_BYTES:
                self._quality = self._findBestQuality(self._image, self.MAX_SIZE_IN_BYTES)
            return self._getBytes(self._image, self.quality())
        else:
            return self._originalImageBytes

    def clone(self):
        clonedImage = type(self)(self._originalImageBytes, self._allowProcessing)

        if self._allowProcessing:
            if self.quality() != 100:
                clonedImage.setQuality(self.quality())

        return clonedImage

    def _getBytes(self, image, quality=100):
        """
        Retorna los bytes de un Image.

        @param image: el Image del cual retornar los bytes.
        @param quality: la calidad con la cual guardar la imagen.
        """
        buffer = io.BytesIO()
        image.save(buffer, "JPEG", quality=quality, optimize=True)
        return buffer.getvalue()

    def _findBestQuality(self, image, maxSizeInBytes):
        """
        Dado un Image y un tamaño máximo en bytes, retorna un int con la mejor calidad posible para la imagen asegurando que el
        tamaño resultante de la misma sea menor o igual al tamaño máximo en bytes.
        """
        for quality in range(100, -1, -1):
            imageBytes = self._getBytes(image, quality)

            if len(imageBytes) <= maxSizeInBytes:
                return quality

        raise Exception("Esto no debería pasar: no se encontró un nivel de compresión en el rango 0-100 capaz de reducir "
                        "lo suficiente el tamaño de la imagen.")


class CoverImage(AbstractEpubBaseImage):
    WIDTH = 600
    HEIGHT = 900
    MAX_SIZE_IN_BYTES = 300 * 1000

    WHITE_LOGO = 0
    BLACK_LOGO = 1
    GLOW_LOGO = 2
    NO_LOGO = 3

    # Dimensiones y tamaño de la imagen requerida para poner en la web.
    WIDTH_FOR_WEB = 400
    HEIGHT_FOR_WEB = 600
    MAX_SIZE_IN_BYTES_FOR_WEB = 100 * 1000

    # Las cubiertas transparentes solamente con los logos.
    # Key: la constante identificando al logo.
    # Value: un Image.
    _LOGOS_COVER = {}

    # Los logos en imágenes más pequeñas.
    # Key: la constante identificando al logo.
    # Value: los bytes con el logo.
    _LOGOS_PREVIEW = {}

    def __init__(self, file, allowProcessing=True):
        super().__init__(file, allowProcessing)
        self._logo = CoverImage.NO_LOGO

    @staticmethod
    def logoPreviewToBytes(logo):
        if not CoverImage._LOGOS_PREVIEW:
            CoverImage._loadLogosPreview()

        return CoverImage._LOGOS_PREVIEW[logo]

    def insertLogo(self, logo):
        """
        Inserta un logo de epublibre en la imagen.

        @param logo: uno de estos posibles valores: WHITE_LOGO, BLACK_LOGO, GLOW_LOGO.
        """
        if not self._allowProcessing:
            raise ValueError("Debe permitirse el procesamiento de la imagen para poder insertarle un logo.")

        if not CoverImage._LOGOS_COVER:
            self._loadLogosCover()

        self._image = self._originalImage.copy()

        logoImage = CoverImage._LOGOS_COVER[logo]
        self._image.paste(logoImage, mask=logoImage)

        self._logo = logo

        # Ojo: al recargar la imagen, ahora la calidad vuelve a ser 100!
        self._quality = 100

    def logo(self):
        return self._logo

    def toBytesForWeb(self):
        if not self._allowProcessing:
            raise ValueError("Debe permitirse el procesamiento de la imagen para poder generar la cubierta para la web.")

        image = self._image.resize((CoverImage.WIDTH_FOR_WEB, CoverImage.HEIGHT_FOR_WEB), resample=Image.ANTIALIAS)

        # Veo primero si con la calidad actual que tiene la cubierta puedo generar una para la web que no sobrepase
        # el tamaño máximo. Caso contrario, busco la mejor calidad.
        imageBytes = self._getBytes(image, self.quality())
        if len(imageBytes) <= CoverImage.MAX_SIZE_IN_BYTES_FOR_WEB:
            return imageBytes
        else:
            quality = self._findBestQuality(image, CoverImage.MAX_SIZE_IN_BYTES_FOR_WEB)
            return self._getBytes(image, quality)

    def clone(self):
        coverImage = CoverImage(self._originalImageBytes, self._allowProcessing)

        if self._allowProcessing:
            if self.logo() != CoverImage.NO_LOGO:
                coverImage.insertLogo(self.logo())

            if self.quality() != 100:
                coverImage.setQuality(self.quality())

        return coverImage

    @staticmethod
    def _loadLogosPreview():
        CoverImage._LOGOS_PREVIEW[CoverImage.WHITE_LOGO] = files.EpubBaseFiles.getFile(files.EpubBaseFiles.WHITE_LOGO_PREVIEW)
        CoverImage._LOGOS_PREVIEW[CoverImage.BLACK_LOGO] = files.EpubBaseFiles.getFile(files.EpubBaseFiles.BLACK_LOGO_PREVIEW)
        CoverImage._LOGOS_PREVIEW[CoverImage.GLOW_LOGO] = files.EpubBaseFiles.getFile(files.EpubBaseFiles.GLOW_LOGO_PREVIEW)

    def _loadLogosCover(self):
        CoverImage._LOGOS_COVER[CoverImage.WHITE_LOGO] = Image.open(io.BytesIO(files.EpubBaseFiles.getFile(files.EpubBaseFiles.WHITE_LOGO_FOR_COVER)))
        CoverImage._LOGOS_COVER[CoverImage.BLACK_LOGO] = Image.open(io.BytesIO(files.EpubBaseFiles.getFile(files.EpubBaseFiles.BLACK_LOGO_FOR_COVER)))
        CoverImage._LOGOS_COVER[CoverImage.GLOW_LOGO] = Image.open(io.BytesIO(files.EpubBaseFiles.getFile(files.EpubBaseFiles.GLOW_LOGO_FOR_COVER)))


class AuthorImage(AbstractEpubBaseImage):
    WIDTH = 320
    HEIGHT = 400
    MAX_SIZE_IN_BYTES = 300 * 1000


class InvalidDimensionsError(Exception):
    pass


class MaxSizeExceededError(Exception):
    pass


class ProgressiveImageError(Exception):
    pass