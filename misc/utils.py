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

import math

from PyQt4 import QtCore, QtGui

import version


class Utilities:

    @staticmethod
    def orderByLastName(name):
        """
        Invierte un nombre en formato "nombre apellido" en "apellido, nombre".
        Ejemplo: "Edgar Allan Poe" es convertido en: "Poe, Edgar Allan".

        @param name: el nombre a convertir.

        @return: un string con el nombre convertido.
        """
        words = name.split(" ")
        if len(words) > 1:
            pivot = math.ceil(len(words) / 2)
            orderedName = []

            words[-1] += ","

            for i in range(pivot, len(words)):
                orderedName.append(words[i])

            for i in range(pivot):
                orderedName.append(words[i])

            return " ".join(orderedName)
        else:
            return name

    @staticmethod
    def enum(**enums):
        """
        Implementa una enumeración.
        http://stackoverflow.com/questions/36932/whats-the-best-way-to-implement-an-enum-in-python
        """
        return type("Enum", (), enums)

    @staticmethod
    def displayStdErrorDialog(message, details):
        msgBox = QtGui.QMessageBox(QtGui.QApplication.activeWindow())
        msgBox.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint)
        msgBox.setModal(True)
        msgBox.setIcon(QtGui.QMessageBox.Critical)
        msgBox.setWindowTitle(version.APP_NAME)
        msgBox.setText(message)

        if details:
            msgBox.setDetailedText(details)

        msgBox.setStandardButtons(QtGui.QMessageBox.Close)
        msgBox.exec()







