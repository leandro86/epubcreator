from PyQt4 import QtCore, QtGui

import version


def displayStdErrorDialog(message, details=None):
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


def insertNewLines(text, every):
    """
    Inserta saltos de línea en un texto cada cierta cantidad de caracteres.
    Los saltos de línea se insertan luego de algún espacio, de manera tal de no cortar
    una palabra a la mitad.

    @param text: un string con el texto.
    @param every: un int que indica cada cuántos caracteres se inserta un salto de línea.

    @return: un string con el texto con los saltos de línea.
    """
    lines = []
    previousNewLinePos = 0
    spacePos = text.find(" ")

    while spacePos != -1:
        if spacePos - previousNewLinePos >= every:
            # El espacio lo dejo al final de la línea, en lugar de copiarlo a la línea de abajo.
            lines.append(text[previousNewLinePos:spacePos + 1])
            previousNewLinePos = spacePos + 1

        spacePos = text.find(" ", spacePos + 1)

    lines.append(text[previousNewLinePos:])

    return "\n".join(lines)