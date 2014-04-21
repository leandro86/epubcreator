import os

from PyQt4 import QtGui


class CoverImage():
    WIDTH = 600
    HEIGHT = 900
    MAX_SIZE_IN_KB = 300

    def __init__(self, file):
        with open(file, "rb") as f:
            self._rawBytes = f.read()

        self._image = QtGui.QImage.fromData(self._rawBytes)

        if self._image.width() != CoverImage.WIDTH or self._image.height() != CoverImage.HEIGHT:
            raise InvalidDimensionsError()

        if os.path.getsize(file) / 1000 > CoverImage.MAX_SIZE_IN_KB:
            raise MaxSizeExceededError()

    def toPixMap(self):
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(self._rawBytes)
        return pixmap

    def toBytes(self):
        return self._rawBytes


class InvalidDimensionsError(Exception):
    pass


class MaxSizeExceededError(Exception):
    pass