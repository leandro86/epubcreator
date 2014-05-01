import unittest
import random
import io

from PIL import Image

from epubcreator.epubbase import images


class CoverImageTest(unittest.TestCase):
    def test_can_load_image_when_dimensions_and_size_are_ok_and_allow_processing_is_false(self):
        imageBytes = self._saveImage(self._createImage(600, 900))
        coverImage = images.CoverImage(imageBytes, allowProcessing=False)

        self.assertEqual(type(coverImage), images.CoverImage)

    def test_image_size_too_big_raises_exception_when_allow_processing_is_false(self):
        image = self._createImage(600, 900)

        data = image.load()

        # Modifico los pixeles con diferentes colores para incrementar de tamaño la imagen.
        for y in range(image.size[1]):
            for x in range(image.size[0]):
                data[x, y] = (0, 0, random.randint(0, 255))

        imageBytes = self._saveImage(image)

        self.assertRaises(images.MaxSizeExceededError, lambda: images.CoverImage(imageBytes, allowProcessing=False))

    def test_image_with_wrong_dimensions_raises_exception_when_allow_processing_is_false(self):
        imageBytes = self._saveImage(self._createImage(50, 50))

        self.assertRaises(images.InvalidDimensionsError, lambda: images.CoverImage(imageBytes, allowProcessing=False))

    def test_image_is_not_modified_when_allow_processing_is_false(self):
        image = self._createImage(600, 900)
        data = image.load()

        data[0, 0] = (123, 21, 90)
        data[0, 1] = (150, 232, 9)
        data[0, 2] = (111, 13, 45)
        data[0, 3] = (8, 214, 78)

        imageBytes = self._saveImage(image)

        self.assertEqual(imageBytes, images.CoverImage(imageBytes, allowProcessing=False).toBytes())

    def test_can_only_load_jpg_images_when_allow_processing_is_false(self):
        image = self._createImage(600, 900)

        imageBytes = self._saveImage(image, "BMP")
        self.assertRaises(ValueError, lambda: images.CoverImage(imageBytes, allowProcessing=False))

        imageBytes = self._saveImage(image, "PNG")
        self.assertRaises(ValueError, lambda: images.CoverImage(imageBytes, allowProcessing=False))

        imageBytes = self._saveImage(image, "JPEG")
        self.assertEqual(type(images.CoverImage(imageBytes, allowProcessing=False)), images.CoverImage)

    def test_cannot_load_progressive_image_when_allow_processing_is_false(self):
        imageBytes = self._saveImage(self._createImage(600, 900), progressive=True)

        self.assertRaises(images.ProgressiveImageError, lambda: images.CoverImage(imageBytes, allowProcessing=False))

    def test_image_with_wrong_dimensions_is_scaled_when_allow_processing_is_true(self):
        imageBytes = self._saveImage(self._createImage(500, 480))

        coverImage = images.CoverImage(imageBytes)
        resizedCoverImage = Image.open(io.BytesIO(coverImage.toBytes()))

        self.assertEqual(resizedCoverImage.size, (600, 900))

    def test_can_load_any_supported_image_format_when_allow_processing_is_true(self):
        image = self._createImage(600, 900)

        imageBytes = self._saveImage(image, "BMP")
        self.assertEqual(type(images.CoverImage(imageBytes)), images.CoverImage)

        imageBytes = self._saveImage(image, "PNG")
        self.assertEqual(type(images.CoverImage(imageBytes)), images.CoverImage)

        imageBytes = self._saveImage(image, "JPEG")
        self.assertEqual(type(images.CoverImage(imageBytes)), images.CoverImage)

    def test_can_load_progressive_image_when_allow_processing_is_true(self):
        imageBytes = self._saveImage(self._createImage(600, 900), progressive=True)

        self.assertEqual(type(images.CoverImage(imageBytes)), images.CoverImage)

    def test_image_quality_is_automatically_lowered_when_size_exceeds_max_size_and_allow_processing_is_true(self):
        image = self._createImage(600, 600)

        data = image.load()

        # Modifico los pixeles con diferentes colores para incrementar de tamaño la imagen.
        for y in range(image.size[1]):
            for x in range(image.size[0]):
                data[x, y] = (0, 0, random.randint(0, 255))

        imageBytes = self._saveImage(image)
        coverImage = images.CoverImage(imageBytes)

        self.assertLessEqual(len(coverImage.toBytes()), images.CoverImage.MAX_SIZE_IN_BYTES)
        self.assertNotEqual(coverImage.quality(), 100)

    def test_image_quality_is_not_automatically_lowered_when_was_manually_set_and_its_size_is_below_max_size_and_allow_processing_is_true(self):
        image = self._createImage(50, 50)

        data = image.load()

        # Modifico los pixeles con diferentes colores para incrementar de tamaño la imagen.
        for y in range(image.size[1]):
            for x in range(image.size[0]):
                data[x, y] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        imageBytes = self._saveImage(image)
        coverImage = images.CoverImage(imageBytes)
        coverImage.setQuality(20)
        quality = coverImage.quality()

        self.assertEqual(coverImage.size(), len(coverImage.toBytes()))
        self.assertEqual(coverImage.quality(), quality)

    def test_change_image_quality_always_operates_in_original_image(self):
        image = self._createImage(50, 50)

        data = image.load()

        # Modifico los pixeles con diferentes colores para incrementar de tamaño la imagen.
        for y in range(image.size[1]):
            for x in range(image.size[0]):
                data[x, y] = (0, 0, random.randint(0, 255))

        imageBytes = self._saveImage(image)
        coverImage1 = images.CoverImage(imageBytes)
        coverImage2 = images.CoverImage(imageBytes)
        coverImage1.setQuality(50)
        coverImage1.setQuality(10)
        coverImage2.setQuality(10)

        self.assertEqual(coverImage1.toBytes(), coverImage2.toBytes())

    def test_logo_insertion(self):
        imageBytes = self._saveImage(self._createImage(100, 100))

        coverImage = images.CoverImage(imageBytes)
        coverImageWithNoLogoBytes = coverImage.toBytes()

        # ¡Cuidado el logo que elijo para hacer el test! Por defecto, al crear un objeto Image, este
        # se llena de pixeles negros, con lo cual si le inserto el logo negro, el test va a fallar! La otra
        # opción sería llenar el Image con pixeles de otro color si quisiera probar con el logo negro...
        coverImage.insertLogo(images.CoverImage.WHITE_LOGO)

        coverImageWithLogoBytes = coverImage.toBytes()

        self.assertNotEqual(coverImageWithLogoBytes, coverImageWithNoLogoBytes)

    def test_cover_for_web(self):
        image = self._createImage(600, 900)

        data = image.load()

        # Modifico los pixeles con diferentes colores para incrementar de tamaño la imagen.
        for y in range(image.size[1]):
            for x in range(image.size[0]):
                data[x, y] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        imageBytes = self._saveImage(image)
        coverImage = images.CoverImage(imageBytes)
        coverImageBytesForWeb = coverImage.toBytesForWeb()
        coverImageForWeb = Image.open(io.BytesIO(coverImageBytesForWeb))

        self.assertEqual(coverImageForWeb.size, (400, 600))
        self.assertLessEqual(len(coverImageBytesForWeb), 100 * 1000)

    def test_can_load_image_in_mode_P_and_save_it_as_jpg(self):
        # Por defecto, _saveImage guarda la imagen en formato jpg, pero jpg no soporta el modo "P", por eso
        # es que debo guardarla como png, que para propósitos del test no tiene importancia: lo único que me
        # interesa es que CoverImage sea capaz de abrir una imagen en modo "P" y poder guardarla como jpg.
        imageBytes = self._saveImage(self._createImage(600, 900, mode="P"), imageFormat="PNG")

        coverImage = images.CoverImage(imageBytes)

        self.assertTrue(len(coverImage.toBytes()) > 0)

    def _createImage(self, width, height, mode="RGB"):
        return Image.new(mode, (width, height))

    def _saveImage(self, image, imageFormat="JPEG", progressive=False):
        buffer = io.BytesIO()

        if not progressive:
            # No puedo poner progressive en False: con que solo aparezca el kwarg "progressive" (sin importar el
            # valor que tenga), ya guarda la imagen como progresiva...
            image.save(buffer, imageFormat, quality=100)
        else:
            image.save(buffer, imageFormat, quality=100, progressive=True)

        return buffer.getvalue()


if __name__ == '__main__':
    unittest.main()