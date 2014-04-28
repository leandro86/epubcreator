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
        coverImage.insertLogo(images.CoverImage.BLACK_LOGO)
        coverImageWithLogoBytes = coverImage.toBytes()

        self.assertNotEqual(coverImageWithLogoBytes, coverImageWithNoLogoBytes)

    def _createImage(self, width, height):
        return Image.new("RGB", (width, height))

    def _saveImage(self, image, imageFormat="JPEG"):
        buffer = io.BytesIO()
        image.save(buffer, imageFormat, quality=100)
        return buffer.getvalue()


if __name__ == '__main__':
    unittest.main()