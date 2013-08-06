# -*- coding: utf-8 -*-

# Copyright (C) 2013 Leandro
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
        iniPath = os.path.join(QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.DataLocation),
                               "epubcreator.ini")
        super().__init__(iniPath, QtCore.QSettings.IniFormat)