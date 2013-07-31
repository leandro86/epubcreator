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

from PyQt4 import QtGui

from gui.forms.compiled import preferences_dialog


class Preferences(QtGui.QDialog, preferences_dialog.Ui_Preferences):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)

        self.accepted.connect(self._savePreferencesAndClose)

    def _savePreferencesAndClose(self):
        for i in range(self.stackedPreferences.count()):
            preferenceWidget = self.stackedPreferences.widget(i)
            preferenceWidget.saveSettings()