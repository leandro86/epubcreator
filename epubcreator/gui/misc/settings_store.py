import os

from PyQt4 import QtCore, QtGui


class SettingsStore(QtCore.QSettings):
    _SETTINGS_GROUP = "userPreferences"

    _EDITOR_SETTING = "{0}/editor".format(_SETTINGS_GROUP)
    _SIGIL_PATH_SETTING = "{0}/sigilPath".format(_SETTINGS_GROUP)

    _EPUBBASE_INCLUDE_OPTIONAL_FILES_SETTING = "{0}/epubBaseIncludeOptionalFiles".format(_SETTINGS_GROUP)

    _DOCX_IGNORE_EMPTY_PARAGRAPHS_SETTING = "{0}/docxIgnoreEmptyParagraphs".format(_SETTINGS_GROUP)

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
    def epubBaseIncludeOptionalFiles(self):
        return self.value(SettingsStore._EPUBBASE_INCLUDE_OPTIONAL_FILES_SETTING, "true") == "true"

    @epubBaseIncludeOptionalFiles.setter
    def epubBaseIncludeOptionalFiles(self, value):
        self.setValue(SettingsStore._EPUBBASE_INCLUDE_OPTIONAL_FILES_SETTING, value)

    @property
    def docxIgnoreEmptyParagraphs(self):
        return self.value(SettingsStore._DOCX_IGNORE_EMPTY_PARAGRAPHS_SETTING, "true") == "true"

    @docxIgnoreEmptyParagraphs.setter
    def docxIgnoreEmptyParagraphs(self, value):
        self.setValue(SettingsStore._DOCX_IGNORE_EMPTY_PARAGRAPHS_SETTING, value)

    def __init__(self):
        iniPath = os.path.join(QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.DataLocation), "epubcreator.ini")
        super().__init__(iniPath, QtCore.QSettings.IniFormat)