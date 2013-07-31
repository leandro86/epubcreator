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

import platform

from PyQt4 import QtGui, QtCore

from gui.forms.compiled import preferences_general_widget, preferences_docx_widget
from misc import settings_store


class PreferencesAbstract(QtGui.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

    def saveSettings(self):
        raise NotImplemented


class GeneralPreferences(PreferencesAbstract, preferences_general_widget.Ui_GeneralPreferences):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.changeSigilPathButton.clicked.connect(self._changeSigilPath)

        self._loadSettings()

    def saveSettings(self):
        settings = settings_store.SettingsStore()

        settings.editor = self.editorInput.text().strip()
        settings.sigilPath = self.sigilPathInput.text().strip()

    def _loadSettings(self):
        settings = settings_store.SettingsStore()

        self.editorInput.setText(settings.editor)
        self.sigilPathInput.setText(settings.sigilPath)

    def _changeSigilPath(self):
        dialogFilter = "Sigil (sigil.exe)"

        if platform.system() == "Linux":
            dialogFilter = "Sigil (sigil)"
        elif platform.system() == "Darwin":
            dialogFilter = "Sigil (Sigil.app)"

        print(platform.system())

        fileName = QtGui.QFileDialog.getOpenFileName(self, "", "", dialogFilter)
        if fileName:
            self.sigilPathInput.setText(fileName)


class DocxPreferences(PreferencesAbstract, preferences_docx_widget.Ui_DocxPreferences):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self._loadSettings()

    def saveSettings(self):
        settings = settings_store.SettingsStore()

        settings.docxIgnoreEmptyParagraphs = self.ignoreEmptyParagraphsInput.isChecked()

    def _loadSettings(self):
        settings = settings_store.SettingsStore()

        self.ignoreEmptyParagraphsInput.setCheckState(QtCore.Qt.Checked if settings.docxIgnoreEmptyParagraphs else
                                                                        QtCore.Qt.Unchecked)