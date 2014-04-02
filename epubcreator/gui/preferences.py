from PyQt4 import QtGui

from epubcreator.gui.forms import preferences_dialog_ui


class Preferences(QtGui.QDialog, preferences_dialog_ui.Ui_Preferences):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.accepted.connect(self._savePreferencesAndClose)

    def _savePreferencesAndClose(self):
        for i in range(self.stackedPreferences.count()):
            preferenceWidget = self.stackedPreferences.widget(i)
            preferenceWidget.saveSettings()