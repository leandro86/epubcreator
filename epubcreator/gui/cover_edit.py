from PyQt4 import QtGui, QtCore

from epubcreator.gui.forms import cover_edit_dialog_ui
from epubcreator.epubbase import images, names


class CoverEdit(QtGui.QDialog, cover_edit_dialog_ui.Ui_Dialog):
    _LOGOS = {}

    def __init__(self, coverImage, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._extendUi()

        self._coverImage = coverImage
        self._logoImageWidgetsToLogos = {self.logo1Image: images.CoverImage.BLACK_LOGO,
                                         self.logo2Image: images.CoverImage.WHITE_LOGO,
                                         self.logo3Image: images.CoverImage.GLOW_LOGO}

        self._updateImage()
        self._connectSignals()

    def _compressImage(self, quality):
        self._coverImage.setQuality(quality)
        self._updateImage()

    def _updateImage(self, compressIfNecessary=False):
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(self._coverImage.toBytes(compressIfNecessary=compressIfNecessary))
        self.coverImage.setPixmap(pixmap)

        imgSizeInBytes = self._coverImage.size()
        if imgSizeInBytes > images.CoverImage.MAX_SIZE_IN_BYTES:
            self.imageSizeLabel.setStyleSheet("color: red")
        else:
            self.imageSizeLabel.setStyleSheet("")
        self.imageSizeLabel.setText("{0} kB".format(str(imgSizeInBytes // 1000)))

        self.qualityInput.blockSignals(True)
        self.qualityInput.setValue(self._coverImage.quality())
        self.qualityInput.blockSignals(False)

    def _insertLogo(self):
        self._coverImage.insertLogo(self._logoImageWidgetsToLogos[self.sender()])
        self._updateImage(compressIfNecessary=True)

    def _logoImageApplyStyle(self):
        self.sender().setStyleSheet("border: 2px solid red")

    def _logoImageRemoveStyle(self):
        self.sender().setStyleSheet("")

    def _extendUi(self):
        # Quiero que el diálogo tenga los botones para minimizarlo y maximizarlo, y parece que
        # no tengo forma de setearlo desde el qt designer.
        self.setWindowFlags(QtCore.Qt.Window)

        if not CoverEdit._LOGOS:
            CoverEdit._LOGOS[images.CoverImage.BLACK_LOGO] = QtGui.QImage(names.getFullPathToFile(names.BLACK_LOGO_PREVIEW))
            CoverEdit._LOGOS[images.CoverImage.WHITE_LOGO] = QtGui.QImage(names.getFullPathToFile(names.WHITE_LOGO_PREVIEW))
            CoverEdit._LOGOS[images.CoverImage.GLOW_LOGO] = QtGui.QImage(names.getFullPathToFile(names.GLOW_LOGO_PREVIEW))

        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(CoverEdit._LOGOS[images.CoverImage.BLACK_LOGO])
        self.logo1Image.setPixmap(pixmap)

        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(CoverEdit._LOGOS[images.CoverImage.WHITE_LOGO])
        self.logo2Image.setPixmap(pixmap)

        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(CoverEdit._LOGOS[images.CoverImage.GLOW_LOGO])
        self.logo3Image.setPixmap(pixmap)

    def _connectSignals(self):
        for logoImage in self._logoImageWidgetsToLogos:
            logoImage.entered.connect(self._logoImageApplyStyle)
            logoImage.left.connect(self._logoImageRemoveStyle)
            logoImage.clicked.connect(self._insertLogo)

        self.qualityInput.valueChanged.connect(self._compressImage)