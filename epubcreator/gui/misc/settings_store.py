import os

from PyQt4 import QtCore, QtGui


class SettingsStore(QtCore.QSettings):
    _SETTINGS_GROUP = "userPreferences"

    _EDITOR_SETTING = "{0}/{1}".format(_SETTINGS_GROUP, "editor")
    _SIGIL_PATH_SETTING = "{0}/{1}".format(_SETTINGS_GROUP, "sigilPath")

    _DOCX_IGNORE_EMPTY_PARAGRAPHS_SETTING = "{0}/{1}".format(_SETTINGS_GROUP, "docxIgnoreEmptyParagraphs")

    @property
    def editor(self):
        return self.value(SettingsStore._EDITOR_SETTING, "")

    @editor.setter
    def editor(self, value):
        self.setValue(SettingsStore._EDITOR_SETTING, value)

    @property
    def sigilPath(self):
        return self.value(SettingsStore._SIGIL_PATH_SETTING, "")

    @sigilPath.setter
    def sigilPath(self, value):
        self.setValue(SettingsStore._SIGIL_PATH_SETTING, value)

    @property
    def docxIgnoreEmptyParagraphs(self):
        return self.value(SettingsStore._DOCX_IGNORE_EMPTY_PARAGRAPHS_SETTING, "true") == "true"

    @docxIgnoreEmptyParagraphs.setter
    def docxIgnoreEmptyParagraphs(self, value):
        self.setValue(SettingsStore._DOCX_IGNORE_EMPTY_PARAGRAPHS_SETTING, value)

    def __init__(self):
        iniPath = os.path.join(QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.DataLocation), "epubcreator.ini")
        super().__init__(iniPath, QtCore.QSettings.IniFormat)