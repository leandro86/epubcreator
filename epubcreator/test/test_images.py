import unittest
import sys

from PyQt4 import QtGui, QtCore

from epubcreator.epubbase import images


class CoverImageTest(unittest.TestCase):
    def test_can_load_image_when_dimensions_and_size_are_ok_and_allow_processing_is_false(self):
        # Necesito esta línea para que se cargue el plugin que me permite guardar en formato jpg.
        app = QtCore.QCoreApplication(sys.argv)

        image = QtGui.QImage(600, 900, QtGui.QImage.Format_ARGB32)

        buffer = QtCore.QBuffer()
        image.save(buffer, "JPG")

        coverImage = images.CoverImage(buffer.data().data(), allowProcessing=False)
        self.assertEqual(type(coverImage), images.CoverImage)

    def test_image_size_too_big_raises_exception_when_allow_processing_is_false(self):
        # Necesito esta línea para que se cargue el plugin que me permite guardar en formato jpg.
        app = QtCore.QCoreApplication(sys.argv)

        image = QtGui.QImage(600, 900, QtGui.QImage.Format_ARGB32)

        for y in range(900):
            for x in range(600):
                image.setPixel(x, y, y * x)

        buffer = QtCore.QBuffer()
        image.save(buffer, "JPG", 100)

        self.assertRaises(images.MaxSizeExceededError, lambda: images.CoverImage(buffer.data().data(), allowProcessing=False))

    def test_image_with_wrong_dimensions_raises_exception_when_allow_processing_is_false(self):
        # Necesito esta línea para que se cargue el plugin que me permite guardar en formato jpg.
        app = QtCore.QCoreApplication(sys.argv)

        image = QtGui.QImage(50, 50, QtGui.QImage.Format_ARGB32)

        buffer = QtCore.QBuffer()
        image.save(buffer, "JPG")

        self.assertRaises(images.InvalidDimensionsError, lambda: images.CoverImage(buffer.data().data(), allowProcessing=False))

    def test_image_is_not_modified_when_allow_processing_is_false(self):
        # Necesito esta línea para que se cargue el plugin que me permite guardar en formato jpg.
        app = QtCore.QCoreApplication(sys.argv)

        image = QtGui.QImage(600, 900, QtGui.QImage.Format_ARGB32)
        image.setPixel(10, 10, 255)
        image.setPixel(100, 255, 120)
        image.setPixel(500, 766, 23)
        image.setPixel(120, 364, 214)

        buffer = QtCore.QBuffer()
        image.save(buffer, "JPG")
        originalImageBytes = buffer.data().data()

        self.assertEqual(originalImageBytes, images.CoverImage(originalImageBytes, allowProcessing=False).toBytes())

    def test_can_only_load_jpg_images_when_allow_processing_is_false(self):
        # Necesito esta línea para que se cargue el plugin que me permite guardar en formato jpg.
        app = QtCore.QCoreApplication(sys.argv)

        image = QtGui.QImage(600, 900, QtGui.QImage.Format_ARGB32)

        buffer = QtCore.QBuffer()
        image.save(buffer, "BMP")
        self.assertRaises(ValueError, lambda: images.CoverImage(buffer.data().data(), allowProcessing=False))

        buffer = QtCore.QBuffer()
        image.save(buffer, "PNG")
        self.assertRaises(ValueError, lambda: images.CoverImage(buffer.data().data(), allowProcessing=False))

        buffer = QtCore.QBuffer()
        image.save(buffer, "JPG")
        self.assertEqual(type(images.CoverImage(buffer.data().data(), allowProcessing=False)), images.CoverImage)

        buffer = QtCore.QBuffer()
        image.save(buffer, "JPEG")
        self.assertEqual(type(images.CoverImage(buffer.data().data(), allowProcessing=False)), images.CoverImage)

    def test_image_with_wrong_dimensions_is_scaled_when_allow_processing_is_true(self):
        # Necesito esta línea para que se cargue el plugin que me permite guardar en formato jpg.
        app = QtCore.QCoreApplication(sys.argv)

        image = QtGui.QImage(500, 480, QtGui.QImage.Format_ARGB32)

        buffer = QtCore.QBuffer()
        image.save(buffer, "JPG")

        coverImage = images.CoverImage(buffer.data().data())

        resizedCoverImage = QtGui.QImage.fromData(coverImage.toBytes())
        self.assertEqual(resizedCoverImage.width(), 600)
        self.assertEqual(resizedCoverImage.height(), 900)

    def test_can_load_any_supported_image_format_when_allow_processing_is_true(self):
        # Necesito esta línea para que se cargue el plugin que me permite guardar en formato jpg.
        app = QtCore.QCoreApplication(sys.argv)

        image = QtGui.QImage(600, 900, QtGui.QImage.Format_ARGB32)

        buffer = QtCore.QBuffer()
        image.save(buffer, "BMP")
        self.assertEqual(type(images.CoverImage(buffer.data().data())), images.CoverImage)

        buffer = QtCore.QBuffer()
        image.save(buffer, "PNG")
        self.assertEqual(type(images.CoverImage(buffer.data().data())), images.CoverImage)

        buffer = QtCore.QBuffer()
        image.save(buffer, "JPG")
        self.assertEqual(type(images.CoverImage(buffer.data().data())), images.CoverImage)

        buffer = QtCore.QBuffer()
        image.save(buffer, "JPEG")
        self.assertEqual(type(images.CoverImage(buffer.data().data())), images.CoverImage)


if __name__ == '__main__':
    unittest.main()
