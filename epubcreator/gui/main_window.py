import os
import subprocess
import re

from PyQt4 import QtGui

from epubcreator.epubbase import ebook
from epubcreator.converters import converter_factory
from epubcreator.misc import settings_store, gui_utils
from epubcreator.gui.forms import main_window_ui
from epubcreator.gui import preferences, about
from epubcreator import version, config


class MainWindow(QtGui.QMainWindow, main_window_ui.Ui_MainWindow):
    _SETTINGS_GROUP = "mainWindow"

    # Las dimensiones y posición de la ventana.
    _MAINWINDOW_GEOMETRY_SETTING = "geometry"
    _MAINWINDOW_STATE_SETTING = "state"

    # El path de la última ubicación desde la cual se abrió un archivo.
    _LAST_FOLDER_OPEN_SETTING = "lastFolderOpen"

    # El path de la última ubicación en la cual se guardó un epub sin asociarle contenido
    # alguno, es decir, que solo se modificaron algunos metadatos y luego se generó el epub, sin
    # abrir ningún docx, ni ningún otro archivo. Cuando se le asocia un contenido al epub, entonces
    # éste se guarda en el mismo directorio donde se encuentra el documento fuente (sea un docx o
    # cualquier otro).
    _LAST_EMPTY_EPUB_OUTPUT_FOLDER_SETTING = "lastEmptyEpubOutputFolder"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # El path del archivo con el cual se está trabajando, es decir, del cual
        # se van a leer las secciones, imágenes, etc., al generar el epub. Puede
        # estar vacío, en cuyo caso al generar el epub solamente se generan los
        # archivos del epubbase.
        self._workingFilePath = ""

        self._lastFolderOpen = ""
        self._lastEmptyEpubOutputFolder = ""

        self.setWindowTitle(version.APP_NAME)

        self._connectSignals()
        self._readSettings()

    def closeEvent(self, event):
        self._writeSettings()

    def _openFile(self):
        fileFilter = "Todos los archivos (*.{0})".format("*.".join(f.FILE_TYPE for f in converter_factory.ConverterFactory.getAllConverters()))
        fileName = QtGui.QFileDialog.getOpenFileName(self, "", self._lastFolderOpen, fileFilter)

        if fileName:
            self._workingFilePath = fileName
            self.setWindowTitle("{0} - {1}".format(os.path.split(fileName)[-1], version.APP_NAME))
            self._lastFolderOpen = os.path.dirname(fileName)
            self._showMessageOnStatusBar("Archivo abierto.", 5000)

    def _generateEpub(self):
        self._showMessageOnStatusBar("Generando ePub...")
        metadata = self.metadataTabManager.getEbookMetadata()

        if metadata:
            settings = settings_store.SettingsStore()
            metadata.editor = settings.editor

            ebookData, rawText = self._prepareEbook()
            eebook = ebook.Ebook(ebookData, metadata, **settings.getAllSettingsForEbook())

            if ebookData:
                self._checkForMissingText(ebookData, rawText)

            # Por defecto guardo el epub en el mismo directorio donde se encuentra
            # el archivo de origen.
            if self._workingFilePath:
                outputDir = os.path.dirname(self._workingFilePath)
            else:
                # Si no estoy trabajando con ningún archivo, debo pedirle al usuario
                # el path donde guardar el epub.
                outputDir = QtGui.QFileDialog.getExistingDirectory(self, "", self._lastEmptyEpubOutputFolder)

            if outputDir:
                if not self._workingFilePath:
                    self._lastEmptyEpubOutputFolder = outputDir

                try:
                    fileName = eebook.save(outputDir)

                    if settings.allowImageProcessing:
                        self._saveImages(outputDir)

                    statusBarMsg = "ePub generado. "

                    if settings.sigilPath:
                        if self._openInSigil(settings.sigilPath, fileName):
                            statusBarMsg += "Abriendo Sigil..."

                    self._showMessageOnStatusBar(statusBarMsg, 5000)
                except IOError as e:
                    gui_utils.displayStdErrorDialog("Ocurrió un error al intentar guardar el epub.", str(e))
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
            gui_utils.displayStdErrorDialog("Sigil no pudo abrirse. Compruebe que la ruta sea correcta.", str(e))
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
        self._lastEmptyEpubOutputFolder = settings.value(MainWindow._LAST_EMPTY_EPUB_OUTPUT_FOLDER_SETTING)

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
        settings.setValue(MainWindow._LAST_EMPTY_EPUB_OUTPUT_FOLDER_SETTING, self._lastEmptyEpubOutputFolder)

        settings.endGroup()

    def _prepareEbook(self):
        settings = settings_store.SettingsStore()

        ebookData = None
        rawText = None

        if self._workingFilePath:
            fileType = os.path.splitext(self._workingFilePath)[1][1:]
            options = settings.getAllSettingsForConverter(fileType)

            converter = converter_factory.ConverterFactory.getConverter(self._workingFilePath, **options)

            ebookData = converter.convert()
            rawText = converter.getRawText()

        return ebookData, rawText

    def _checkForMissingText(self, ebookData, rawText):
        sectionsText = "".join((s.toRawText() for s in ebookData.iterAllSections()))

        # Elimino absolutamente todos los espacios (espacios, tabs, non breaking spaces, etc) al comparar el texto.
        # No solo lo hago porque principalemente lo único que me importa es que no se haya perdido texto en la
        # conversión, sino porque el documento fuente y el texto resultante de la conversión no necesariamente deben
        # coincidir en un 100%: el documento fuente puede contener párrafos en blanco (tal vez con espacios
        # incluso, o no), por ejemplo, que tal vez no haya que convertir.
        isTextMissing = re.sub(r"\s+", "", rawText) != re.sub(r"\s+", "", sectionsText)

        if isTextMissing:
            gui_utils.displayStdErrorDialog("Se ha perdido texto en la conversión. Por favor, repórtalo a los desarrolladores y adjunta "
                                            "el documento fuente.")

    def _saveImages(self, outputDir):
        coverImage = self.metadataTabManager.basicMetadata.getCoverImage()

        if coverImage is not None:
            with open(os.path.join(outputDir, "cover_web.jpg"), "wb") as file:
                file.write(coverImage.toBytesForWeb())

    def _close(self):
        QtGui.qApp.closeAllWindows()
        QtGui.qApp.quit()

    def _showPreferencesDialog(self):
        settings = settings_store.SettingsStore()
        previousAllowImageProcessing = settings.allowImageProcessing

        if preferences.Preferences(self).exec() == QtGui.QDialog.Accepted:
            if previousAllowImageProcessing != settings.allowImageProcessing:
                coverImage = self.metadataTabManager.basicMetadata.getCoverImage()
                authors = self.metadataTabManager.basicMetadata.getAuthors()
                wasAuthorWithImage = False

                if coverImage:
                    self.metadataTabManager.basicMetadata.setCoverImage(None)

                for author in authors:
                    if author.image:
                        wasAuthorWithImage = True
                    author.image = None

                if coverImage or wasAuthorWithImage:
                    gui_utils.displayInformationDialog("La opción para permitir el procesamiento de las imágenes del ePub base ha cambiado de "
                                                       "valor. Debe cargar nuevamente las imágenes de cubierta y autores.")

    def _connectSignals(self):
        self.openFileAction.triggered.connect(self._openFile)
        self.generateEpubAction.triggered.connect(self._generateEpub)
        self.preferencesAction.triggered.connect(self._showPreferencesDialog)
        self.toggleToolBarAction.triggered.connect(self.toolBar.setVisible)
        self.toolBar.visibilityChanged.connect(self.toggleToolBarAction.setChecked)
        self.quitAction.triggered.connect(self._close)
        self.aboutAction.triggered.connect(lambda: about.About(self).exec())
