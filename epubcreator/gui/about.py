from PyQt4 import QtGui, QtCore

from epubcreator.gui.forms import about_dialog_ui
from epubcreator import version


class About(QtGui.QDialog, about_dialog_ui.Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.versionLabel.setText(version.VERSION)
        self.descriptionLabel.setText(version.DESCRIPTION)
        self.qtVersionLabel.setText(QtCore.QT_VERSION_STR)