import platform

from PyQt4 import QtGui, QtCore

from epubcreator.gui.forms import preferences_general_widget_ui, preferences_docx_widget_ui, preferences_epub_widget_ui
from epubcreator.misc import settings_store, gui_utils
from epubcreator.converters.docx import docx_converter
from epubcreator.epubbase import ebook


class PreferencesAbstract(QtGui.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def saveSettings(self):
        raise NotImplemented


class GeneralPreferences(PreferencesAbstract, preferences_general_widget_ui.Ui_GeneralPreferences):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._extendUi()

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

        fileName = QtGui.QFileDialog.getOpenFileName(self, "", "", dialogFilter)
        if fileName:
            self.sigilPathInput.setText(fileName)

    def _extendUi(self):
        self.editorInput.setToolTip(gui_utils.formatTextForTooltip("El alias del editor."))
        self.sigilPathInput.setToolTip(gui_utils.formatTextForTooltip("Si se desea abrir automáticamente con Sigil el epub generado, entonces "
                                                                      "completar este campo con la ruta hacia el ejecutable."))


class DocxPreferences(PreferencesAbstract, preferences_docx_widget_ui.Ui_DocxPreferences):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._extendUi()

        self._loadSettings()

    def saveSettings(self):
        settings = settings_store.SettingsStore()

        settings.docxIgnoreEmptyParagraphs = self.ignoreEmptyParagraphsInput.isChecked()

    def _loadSettings(self):
        settings = settings_store.SettingsStore()

        self.ignoreEmptyParagraphsInput.setCheckState(QtCore.Qt.Checked if settings.docxIgnoreEmptyParagraphs else QtCore.Qt.Unchecked)

    def _extendUi(self):
        description = gui_utils.formatTextForTooltip(docx_converter.DocxConverter.getOptionDescription("ignoreEmptyParagraphs"))
        self.ignoreEmptyParagraphsInput.setToolTip(description)


class EpubPreferences(PreferencesAbstract, preferences_epub_widget_ui.Ui_EpubBasePreferences):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._extendUi()

        self._loadSettings()

    def saveSettings(self):
        settings = settings_store.SettingsStore()

        settings.epubOutputIncludeOptionalFiles = self.includeOptionalFilesInput.isChecked()

    def _loadSettings(self):
        settings = settings_store.SettingsStore()

        self.includeOptionalFilesInput.setCheckState(QtCore.Qt.Checked if settings.epubOutputIncludeOptionalFiles else QtCore.Qt.Unchecked)

    def _extendUi(self):
        description = gui_utils.formatTextForTooltip(ebook.Ebook.getOptionDescription("includeOptionalFiles"))
        self.includeOptionalFilesInput.setToolTip(description)