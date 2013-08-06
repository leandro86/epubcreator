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
import subprocess

from PyQt4 import QtGui, QtCore

from ecreator.transformers import docx_transformer
from ecreator import ebook
from misc import settings_store, utils
from gui.forms.compiled import main_window
from gui import preferences, log_window

class MainWindow(QtGui.QMainWindow, main_window.Ui_MainWindow):

    _SETTINGS_GROUP = "mainWindow"
    _MAINWINDOW_GEOMETRY_SETTING = "geometry"
    _MAINWINDOW_STATE_SETTING = "state"
    _LAST_FOLDER_OPEN_SETTING = "lastFolderOpen"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # El path del archivo con el cual se está trabajando, es decir, del cual
        # se van a leer las secciones, imágenes, etc., al generar el epub. Puede
        # estar vacío, en cuyo caso al generar el epub solamente se generan los
        # archivos del epubbase.
        self._workingFilePath = ""

        # La ventana de log
        self._logWindow = log_window.LogWindow(self)

        # El path de la última ubicación desde la cual se abrió un archivo.
        self._lastFolderOpen = ""

        # Agrego la ventana de log, por defecto oculta.
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self._logWindow)
        self._logWindow.hide()

        self._connectSignals()
        self._readSettings()

    def closeEvent(self, event):
        self._writeSettings()

    def _openFile(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, "", self._lastFolderOpen, "Docx (*.docx)")

        if fileName:
            self._workingFilePath = fileName
            self.setWindowTitle(os.path.split(fileName)[-1])
            self._lastFolderOpen = os.path.dirname(fileName)
            self._showMessageOnStatusBar("Trabajando con: {0}.".format(fileName), 5000)

    def _generateEpub(self):
        self._showMessageOnStatusBar("Generando ePub...")
        metadata = self.metadataTabManager.getEbookMetadata()

        if metadata:
            settings = settings_store.SettingsStore()
            metadata.editor = settings.editor

            files, titles, logMessages = self._prepareEbook()
            eebook = ebook.Ebook(files, titles, metadata)

            # Por defecto guardo el epub en el mismo directorio donde se encuentra
            # el archivo de origen.
            if self._workingFilePath:
                outputDir = os.path.dirname(self._workingFilePath)
            else:
                # Si no estoy trabajando con ningún archivo, debo pedirle al usuario
                # el path donde guardar el epub.
                outputDir = QtGui.QFileDialog.getExistingDirectory(self, "", "")

            if outputDir:
                try:
                    fileName = eebook.save(outputDir)
                    self._logWindow.addlogMessages(logMessages)

                    if logMessages:
                        self._logWindow.show()

                    if settings.sigilPath:
                        self._showMessageOnStatusBar("Abriendo ePub en Sigil...")
                        self._openInSigil(settings.sigilPath, fileName)
                except IOError as e:
                    utils.Utilities.displayStdErrorDialog("Ocurrió un error al intentar guardar el epub.", str(e))

        self._showMessageOnStatusBar("")

    def _openInSigil(self, sigilPath, fileName):
        try:
            subprocess.Popen([sigilPath, fileName])
        except Exception as e:
            utils.Utilities.displayStdErrorDialog("Sigil no pudo abrirse. Compruebe que la ruta sea correcta.", str(e))

    def _showMessageOnStatusBar(self, message, duration=0):
        if not message:
            self.statusBar().clearMessage()
        else:
            self.statusBar().showMessage(message, duration)

    def _readSettings(self):
        settings = settings_store.SettingsStore()
        settings.beginGroup(MainWindow._SETTINGS_GROUP)

        mainWindowGeometry = settings.value(MainWindow._MAINWINDOW_GEOMETRY_SETTING)
        mainWindowState = settings.value(MainWindow._MAINWINDOW_STATE_SETTING)
        self._lastFolderOpen = settings.value(MainWindow._LAST_FOLDER_OPEN_SETTING)

        settings.endGroup()

        if mainWindowGeometry:
            self.restoreGeometry(mainWindowGeometry)

        if mainWindowState:
            self.restoreState(mainWindowState)

    def _writeSettings(self):
        settings = settings_store.SettingsStore()
        settings.beginGroup(MainWindow._SETTINGS_GROUP)

        settings.setValue(MainWindow._MAINWINDOW_GEOMETRY_SETTING, self.saveGeometry())
        settings.setValue(MainWindow._MAINWINDOW_STATE_SETTING, self.saveState())
        settings.setValue(MainWindow._LAST_FOLDER_OPEN_SETTING, self._lastFolderOpen)

        settings.endGroup()

    def _showPreferences(self):
        prefs = preferences.Preferences(self)
        prefs.exec()

    def _prepareEbook(self):
        settings = settings_store.SettingsStore()

        files = []
        titles = []
        logMessages = []

        if self._workingFilePath.endswith(".docx"):
            transformer = docx_transformer.DocxTransformer(self._workingFilePath, settings.docxIgnoreEmptyParagraphs)
            files, titles, logMessages = transformer.transform()

        return files, titles, logMessages

    def _connectSignals(self):
        self.openFileAction.triggered.connect(self._openFile)
        self.generateEpubAction.triggered.connect(self._generateEpub)
        self.preferencesAction.triggered.connect(self._showPreferences)
        self.toggleLogWindowAction.triggered.connect(self._logWindow.setVisible)
        self._logWindow.visibilityChanged.connect(self.toggleLogWindowAction.setChecked)
        self.toggleToolBarAction.triggered.connect(self.toolBar.setVisible)
        self.toolBar.visibilityChanged.connect(self.toggleToolBarAction.setChecked)
        self.quitAction.triggered.connect(QtGui.qApp.quit)
