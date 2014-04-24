import unittest
import random
import sys

from PyQt4 import QtGui, QtCore

from epubcreator.epubbase import images


class CoverImageTest(unittest.TestCase):
    def test_can_load_image_when_dimensions_and_size_are_ok_and_allow_processing_is_false(self):
        # Necesito esta línea para que se cargue el plugin que me permite guardar en formato jpg.
        app = QtCore.QCoreApplication(sys.argv)

        imgBytes = self._getBytes(self._createImage(600, 900))
        coverImage = images.CoverImage(imgBytes, allowProcessing=False)

        self.assertEqual(type(coverImage), images.CoverImage)

    def test_image_size_too_big_raises_exception_when_allow_processing_is_false(self):
        # Necesito esta línea para que se cargue el plugin que me permite guardar en formato jpg.
        app = QtCore.QCoreApplication(sys.argv)

        image = self._createImage(600, 900)

        for y in range(900):
            for x in range(600):
                image.setPixel(x, y, QtGui.qRgb(0, 0, random.randint(0, 255)))

        imgBytes = self._getBytes(image)

        self.assertRaises(images.MaxSizeExceededError, lambda: images.CoverImage(imgBytes, allowProcessing=False))

    def test_image_with_wrong_dimensions_raises_exception_when_allow_processing_is_false(self):
        # Necesito esta línea para que se cargue el plugin que me permite guardar en formato jpg.
        app = QtCore.QCoreApplication(sys.argv)

        imgBytes = self._getBytes(self._createImage(50, 50))

        self.assertRaises(images.InvalidDimensionsError, lambda: images.CoverImage(imgBytes, allowProcessing=False))

    def test_image_is_not_modified_when_allow_processing_is_false(self):
        # Necesito esta línea para que se cargue el plugin que me permite guardar en formato jpg.
        app = QtCore.QCoreApplication(sys.argv)

        image = self._createImage(600, 900)
        image.setPixel(10, 10, 255)
        image.setPixel(100, 255, 120)
        image.setPixel(500, 766, 23)
        image.setPixel(120, 364, 214)

        originalImageBytes = self._getBytes(image)

        self.assertEqual(originalImageBytes, images.CoverImage(originalImageBytes, allowProcessing=False).toBytes())

    def test_can_only_load_jpg_images_when_allow_processing_is_false(self):
        # Necesito esta línea para que se cargue el plugin que me permite guardar en formato jpg.
        app = QtCore.QCoreApplication(sys.argv)

        image = self._createImage(600, 900)

        imgBytes = self._getBytes(image, "BMP")
        self.assertRaises(ValueError, lambda: images.CoverImage(imgBytes, allowProcessing=False))

        imgBytes = self._getBytes(image, "PNG")
        self.assertRaises(ValueError, lambda: images.CoverImage(imgBytes, allowProcessing=False))

        imgBytes = self._getBytes(image, "JPG")
        self.assertEqual(type(images.CoverImage(imgBytes, allowProcessing=False)), images.CoverImage)

        imgBytes = self._getBytes(image, "JPEG")
        self.assertEqual(type(images.CoverImage(imgBytes, allowProcessing=False)), images.CoverImage)

    def test_image_with_wrong_dimensions_is_scaled_when_allow_processing_is_true(self):
        # Necesito esta línea para que se cargue el plugin que me permite guardar en formato jpg.
        app = QtCore.QCoreApplication(sys.argv)

        imgBytes = self._getBytes(self._createImage(500, 480))

        coverImage = images.CoverImage(imgBytes)

        resizedCoverImage = QtGui.QImage.fromData(coverImage.toBytes())
        self.assertEqual(resizedCoverImage.width(), 600)
        self.assertEqual(resizedCoverImage.height(), 900)

    def test_can_load_any_supported_image_format_when_allow_processing_is_true(self):
        # Necesito esta línea para que se cargue el plugin que me permite guardar en formato jpg.
        app = QtCore.QCoreApplication(sys.argv)

        image = self._createImage(600, 900)

        imgBytes = self._getBytes(image, "BMP")
        self.assertEqual(type(images.CoverImage(imgBytes)), images.CoverImage)

        imgBytes = self._getBytes(image, "PNG")
        self.assertEqual(type(images.CoverImage(imgBytes)), images.CoverImage)

        imgBytes = self._getBytes(image, "JPG")
        self.assertEqual(type(images.CoverImage(imgBytes)), images.CoverImage)

        imgBytes = self._getBytes(image, "JPEG")
        self.assertEqual(type(images.CoverImage(imgBytes)), images.CoverImage)

    def test_image_is_compressed_when_size_exceeds_max_size_and_allow_processing_is_true(self):
        # Necesito esta línea para que se cargue el plugin que me permite guardar en formato jpg.
        app = QtCore.QCoreApplication(sys.argv)

        image = self._createImage(600, 600)

        for y in range(600):
            for x in range(600):
                image.setPixel(x, y, QtGui.qRgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

        imgBytes = self._getBytes(image)

        coverImage = images.CoverImage(imgBytes)
        self.assertLessEqual(len(coverImage.toBytes()), images.CoverImage.MAX_SIZE_IN_BYTES)
        self.assertNotEqual(coverImage.quality(), 100)

    def test_image_is_not_compressed_when_was_already_manually_compressed_and_its_size_is_below_max_size_and_allow_processing_is_true(self):
        # Necesito esta línea para que se cargue el plugin que me permite guardar en formato jpg.
        app = QtCore.QCoreApplication(sys.argv)

        image = self._createImage(50, 50)

        for y in range(50):
            for x in range(50):
                image.setPixel(x, y, QtGui.qRgb(0, 0, random.randint(0, 255)))

        imgBytes = self._getBytes(image)
        coverImage = images.CoverImage(imgBytes)

        coverImage.compress(20)
        quality = coverImage.quality()
        self.assertEqual(coverImage.size(), len(coverImage.toBytes()))
        self.assertEqual(coverImage.quality(), quality)

    def _createImage(self, width, height):
        return QtGui.QImage(width, height, QtGui.QImage.Format_ARGB32)

    def _getBytes(self, image, imgFormat="JPG"):
        buffer = QtCore.QBuffer()
        image.save(buffer, imgFormat, 100)
        return buffer.data().data()


if __name__ == '__main__':
    unittest.main()