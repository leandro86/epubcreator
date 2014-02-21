from PyQt4 import QtGui, QtCore

from gui.forms.compiled import about_dialog
import version


class About(QtGui.QDialog, about_dialog.Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.versionLabel.setText(version.VERSION)
        self.descriptionLabel.setText(version.DESCRIPTION)
        self.qtVersionLabel.setText(QtCore.QT_VERSION_STR)