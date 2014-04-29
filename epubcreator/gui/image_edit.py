from PyQt4 import QtGui, QtCore

from epubcreator.gui.forms import image_edit_dialog_ui
from epubcreator.epubbase import images, names


class ImageEdit(QtGui.QDialog, image_edit_dialog_ui.Ui_Dialog):
    COVER = 0
    AUTHOR = 1

    _LOGOS = {}

    def __init__(self, image, imageType=COVER, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._extendUi(imageType)

        if imageType == ImageEdit.COVER:
            self._logoImageWidgetsToLogos = {self.logo1Image: images.CoverImage.BLACK_LOGO,
                                             self.logo2Image: images.CoverImage.WHITE_LOGO,
                                             self.logo3Image: images.CoverImage.GLOW_LOGO}

        self._image = image

        self._updateImage()
        self._connectSignals(imageType)

    def _compressImage(self, quality):
        self._image.setQuality(quality)
        self._updateImage()

    def _updateImage(self, compressIfNecessary=False):
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(self._image.toBytes(compressIfNecessary=compressIfNecessary))
        self.image.setPixmap(pixmap)

        imgSizeInBytes = self._image.size()
        if imgSizeInBytes > images.CoverImage.MAX_SIZE_IN_BYTES:
            self.imageSizeLabel.setStyleSheet("color: red")
        else:
            self.imageSizeLabel.setStyleSheet("")
        self.imageSizeLabel.setText("{0} kB".format(str(imgSizeInBytes // 1000)))

        self.qualityInput.blockSignals(True)
        self.qualityInput.setValue(self._image.quality())
        self.qualityInput.blockSignals(False)

    def _insertLogo(self):
        self._image.insertLogo(self._logoImageWidgetsToLogos[self.sender()])
        self._updateImage(compressIfNecessary=True)

    def _logoImageApplyStyle(self):
        self.sender().setStyleSheet("border: 2px solid red")

    def _logoImageRemoveStyle(self):
        self.sender().setStyleSheet("")

    def _extendUi(self, imageType):
        # Quiero que el diálogo tenga los botones para minimizarlo y maximizarlo, y parece que
        # no tengo forma de setearlo desde el qt designer.
        self.setWindowFlags(QtCore.Qt.Window)

        if imageType == ImageEdit.COVER:
            if not ImageEdit._LOGOS:
                ImageEdit._LOGOS[images.CoverImage.BLACK_LOGO] = QtGui.QPixmap(names.getFullPathToFile(names.BLACK_LOGO_PREVIEW))
                ImageEdit._LOGOS[images.CoverImage.WHITE_LOGO] = QtGui.QPixmap(names.getFullPathToFile(names.WHITE_LOGO_PREVIEW))
                ImageEdit._LOGOS[images.CoverImage.GLOW_LOGO] = QtGui.QPixmap(names.getFullPathToFile(names.GLOW_LOGO_PREVIEW))

            self.logo1Image.setPixmap(ImageEdit._LOGOS[images.CoverImage.BLACK_LOGO])
            self.logo2Image.setPixmap(ImageEdit._LOGOS[images.CoverImage.WHITE_LOGO])
            self.logo3Image.setPixmap(ImageEdit._LOGOS[images.CoverImage.GLOW_LOGO])
        else:
            # La única razón por la que tuve que usar un frame para los logos, en lugar de utilizar
            # directamente un layout: para poder ocultarlo cuando quiero editar la imagen de un autor.
            self.logosFrame.hide()

    def _connectSignals(self, imageType):
        if imageType == ImageEdit.COVER:
            for logoImage in self._logoImageWidgetsToLogos:
                logoImage.entered.connect(self._logoImageApplyStyle)
                logoImage.left.connect(self._logoImageRemoveStyle)
                logoImage.clicked.connect(self._insertLogo)

        self.qualityInput.valueChanged.connect(self._compressImage)