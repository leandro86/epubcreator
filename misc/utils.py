import math
import unicodedata

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

        Ejemplo de uso: enum(RED=1, BLUE=2, GREEN=3)
        """
        #http://stackoverflow.com/questions/36932/whats-the-best-way-to-implement-an-enum-in-python
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

    @staticmethod
    def displayExceptionErrorDialog(exceptionMessage):
        msgBox = QtGui.QMessageBox(QtGui.QApplication.activeWindow())
        msgBox.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint)
        msgBox.setModal(True)
        msgBox.setIcon(QtGui.QMessageBox.Critical)
        msgBox.setWindowTitle(version.APP_NAME)

        # Agrego algunos espacios porque sino el diálogo es muy chico...
        msgBox.setText("Se ha encontrado un problema desconocido.{0}".format(" " * 30))

        msgBox.setInformativeText("Por favor, repórtalo a los desarrolladores.")
        msgBox.setStandardButtons(QtGui.QMessageBox.Close)
        msgBox.setDetailedText(exceptionMessage)
        msgBox.exec()

    @staticmethod
    def purgeString(s):
        """
        Elimina acentos y caracteres no latinos de un string.

        @param s: el string del cual eliminar los caracteres.

        @return: un string con los caracteres eliminados.
        """
        return unicodedata.normalize("NFKD", s).encode('ASCII', 'ignore').decode()






