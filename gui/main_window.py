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

from PyQt4 import QtGui

from ecreator.transformers import docx_transformer
from ecreator import ebook
from misc import settings_store, utils
from gui.forms.compiled import main_window
from gui import preferences

class MainWindow(QtGui.QMainWindow, main_window.Ui_MainWindow):

    _SETTINGS_GROUP = "mainWindow"
    _GEOMETRY_SETTING = "{0}/{1}".format(_SETTINGS_GROUP, "geometry")
    _LAST_FOLDER_OPEN = "{0}/{1}".format(_SETTINGS_GROUP, "lastFolderOpen")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # El path del archivo con el cual se está trabajando, es decir, del cual
        # se van a leer las secciones, imágenes, etc., al generar el epub. Puede
        # estar vacío, en cuyo caso al generar el epub solamente se generan los
        # archivos del epubbase.
        self._workingFilePath = ""

        # El path de la última ubicación desde la cual se abrió un archivo.
        self._lastFolderOpen = ""

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

            files, titles = self._prepareEbook()
            eebook = ebook.Ebook(files, titles, metadata)

            # Por defecto guardo el epub en el mismo directorio donde se encuentra
            # el archivo de origen.
            if self._workingFilePath:
                file = os.path.dirname(self._workingFilePath)
            else:
                # Si no estoy trabajando con ningún archivo, debo pedirle al usuario
                # el path donde guardar el epub.
                file = QtGui.QFileDialog.getExistingDirectory(self, "", "")

            if file:
                try:
                    fileName = eebook.save(file)
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

    def _showMessageOnStatusBar(self, message, duration = 0):
        if not message:
            self.statusBar().clearMessage()
        else:
            self.statusBar().showMessage(message, duration)

    def _readSettings(self):
        settings = settings_store.SettingsStore()
        geometry = settings.value(MainWindow._GEOMETRY_SETTING)
        self._lastFolderOpen = settings.value(MainWindow._LAST_FOLDER_OPEN)

        if geometry:
            self.restoreGeometry(geometry)

    def _writeSettings(self):
        settings = settings_store.SettingsStore()
        settings.setValue(MainWindow._GEOMETRY_SETTING, self.saveGeometry())
        settings.setValue(MainWindow._LAST_FOLDER_OPEN, self._lastFolderOpen)

    def _showPreferences(self):
        prefs = preferences.Preferences(self)
        prefs.exec()

    def _prepareEbook(self):
        settings = settings_store.SettingsStore()

        # Dependiendo del documento de origen a procesar, llama al transformer adecuado y
        # retorna una tupla con dos elementos: una lista de File, y una lista de Title.
        files = []
        titles = []

        if self._workingFilePath.endswith(".docx"):
            transformer = docx_transformer.DocxTransformer(self._workingFilePath, settings.docxIgnoreEmptyParagraphs)
            files, titles = transformer.transform()

        return files, titles

    def _connectSignals(self):
        self.openFileAction.triggered.connect(self._openFile)
        self.generateEpubAction.triggered.connect(self._generateEpub)
        self.preferencesAction.triggered.connect(self._showPreferences)