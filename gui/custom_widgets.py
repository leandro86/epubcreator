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

from PyQt4 import QtCore, Qt, QtGui

class ExtendedQLabel(QtGui.QLabel):

    """Un QLabel que emite la señal "clicked" cuando se realiza click sobre él."""

    clicked = Qt.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def mouseReleaseEvent(self, event):
        self.clicked.emit()


class ExtendedQListWidget(QtGui.QListWidget):

    """Un QListWidget que emite la señal "deleteKeyPressed" cuando se presiona la tecla "delete"."""

    deleteKeyPressed = Qt.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            self.deleteKeyPressed.emit()