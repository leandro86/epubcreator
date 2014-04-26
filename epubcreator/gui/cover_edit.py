from PyQt4 import QtGui, QtCore

from epubcreator.gui.forms import cover_edit_dialog_ui


class CoverEdit(QtGui.QDialog, cover_edit_dialog_ui.Ui_Dialog):
    def __init__(self, coverImage, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._extendUi()

        self._coverImage = coverImage
        self._updateImage()
        self.qualityInput.setValue(self._coverImage.quality())

        self.qualityInput.valueChanged.connect(self._compressImage)

    def _compressImage(self, quality):
        self._coverImage.compress(quality)
        self._updateImage()

    def _updateImage(self):
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(self._coverImage.toBytes(compressIfNeeded=False))
        self.coverImage.setPixmap(pixmap)
        self.imageSizeLabel.setText("{0} kB".format(str(self._coverImage.size() // 1000)))

    def _extendUi(self):
        # Quiero que el diálogo tenga los botones para minimizarlo y maximizarlo, y parece que
        # no tengo forma de setearlo desde el qt designer.
        self.setWindowFlags(QtCore.Qt.Window)