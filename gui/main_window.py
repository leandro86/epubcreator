import os
import subprocess

from PyQt4 import QtGui, QtCore

from ecreator.transformers import docx_transformer
from ecreator import ebook
from misc import settings_store, utils
from gui.forms.compiled import main_window
from gui import preferences, log_window, about
import version
import config


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

        self.setWindowTitle(version.APP_NAME)

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
            self.setWindowTitle("{0} - {1}".format(os.path.split(fileName)[-1], version.APP_NAME))
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

                    statusBarMsg = "ePub generado. "

                    if settings.sigilPath:
                        if self._openInSigil(settings.sigilPath, fileName):
                            statusBarMsg += "Abriendo Sigil..."

                    self._showMessageOnStatusBar(statusBarMsg, 5000)
                except IOError as e:
                    utils.Utilities.displayStdErrorDialog("Ocurrió un error al intentar guardar el epub.", str(e))
                    self._showMessageOnStatusBar("No se pudo generar el ePub.")

    def _openInSigil(self, sigilPath, fileName):
        """
        Abre un epub en sigil.

        @param sigilPath: el path de sigil.
        @param fileName: la ruta del epub a abrir.

        @return: True o False, dependiendo de si sigil pudo abrirse o no.
        """
        try:
            if config.IS_RUNNING_ON_MAC:
                # Un bundle (archivo .app) no puedo abrirlo directamente como si fuera
                # un ejecutable, sino que debo utilizar el comando "open".
                subprocess.Popen(["open", "-a", sigilPath, fileName])
            else:
                subprocess.Popen([sigilPath, fileName])
            return True
        except Exception as e:
            utils.Utilities.displayStdErrorDialog("Sigil no pudo abrirse. Compruebe que la ruta sea correcta.", str(e))
            return False

    def _showMessageOnStatusBar(self, message, duration=0):
        if not message:
            self.statusBar().clearMessage()
        else:
            self.statusBar().showMessage(message, duration)

        # Obligo a mostrar el mensaje en la barra de estado, ya que si
        # previamente empezó a correr un proceso que lleva algo de
        # tiempo, el mensaje se muestra después de que el proceso finalice.
        # Aunque esto solamente pasa en linux y mac, no en windows. Es decir, que
        # en windows esta línea no sería necesaria.
        QtGui.QApplication.processEvents()

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

    def _prepareEbook(self):
        settings = settings_store.SettingsStore()

        files = []
        titles = []
        logMessages = []

        if self._workingFilePath.endswith(".docx"):
            transformer = docx_transformer.DocxTransformer(self._workingFilePath, settings.docxIgnoreEmptyParagraphs)
            files, titles, logMessages = transformer.transform()

        return files, titles, logMessages

    def _close(self):
        QtGui.qApp.closeAllWindows()
        QtGui.qApp.quit()

    def _connectSignals(self):
        self.openFileAction.triggered.connect(self._openFile)
        self.generateEpubAction.triggered.connect(self._generateEpub)
        self.preferencesAction.triggered.connect(lambda: preferences.Preferences(self).exec())
        self.toggleLogWindowAction.triggered.connect(self._logWindow.setVisible)
        self._logWindow.visibilityChanged.connect(self.toggleLogWindowAction.setChecked)
        self.toggleToolBarAction.triggered.connect(self.toolBar.setVisible)
        self.toolBar.visibilityChanged.connect(self.toggleToolBarAction.setChecked)
        self.quitAction.triggered.connect(self._close)
        self.aboutAction.triggered.connect(lambda: about.About(self).exec())
