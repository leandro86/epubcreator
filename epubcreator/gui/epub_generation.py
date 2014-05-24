from PyQt4 import QtGui, QtCore

from epubcreator.gui.forms import epub_generation_dialog_ui
from epubcreator.misc import settings_store


class EpubGeneration(QtGui.QDialog, epub_generation_dialog_ui.Ui_EpubGeneration):
    _SETTINGS_GROUP = "epubGenerationDialog"

    # Indica si el diálogo debe cerrase automáticamente cuando no hubo warnings.
    _AUTO_CLOSE_DIALOG_SETTING = "autoClose"

    _QWIDGETSIZE_MAX = (1 << 24) - 1

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._extendUi()

        self._readAutoCloseSetting()

        self.closeDialogInput.stateChanged.connect(self._writeAutoCloseSetting)

    def ok(self, warnings=None):
        self.imageLabel.movie().stop()
        self.buttonBox.setEnabled(True)
        self.setWindowTitle("Epub Generado")

        if not warnings:
            if self.closeDialogInput.isChecked():
                self.close()
            else:
                self.imageLabel.setPixmap(QtGui.QPixmap(":/ok.png"))
                self.infoLabel.setStyleSheet("color: #49950F")
                self.infoLabel.setText("Epub generado!")
        else:
            self.imageLabel.setPixmap(QtGui.QPixmap(":/warning.png"))
            self.infoLabel.setStyleSheet("color: #C57E14")
            self.infoLabel.setText("Epub generado. Revise los mensajes de advertencia.")

            self.setMinimumSize(0, 0)
            self.setMaximumSize(EpubGeneration._QWIDGETSIZE_MAX, EpubGeneration._QWIDGETSIZE_MAX)

            self._showWarnings(warnings)
            self.resize(self.width(), 0)

    def _showWarnings(self, warnings):
        gridLayout = QtGui.QVBoxLayout()

        groupbox = QtGui.QGroupBox("Advertencias", self)
        groupbox.setAlignment(QtCore.Qt.AlignHCenter)
        font = QtGui.QFont()
        font.setBold(True)
        groupbox.setFont(font)
        groupbox.setLayout(gridLayout)
        groupbox.sizePolicy().setVerticalPolicy(QtGui.QSizePolicy.Fixed)

        table = QtGui.QTableWidget(self)
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["", ""])
        table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        table.setMinimumHeight(170)
        table.horizontalHeader().setVisible(True)
        table.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        table.horizontalHeader().setStretchLastSection(True)
        table.verticalHeader().setVisible(False)
        table.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        table.setWordWrap(True)
        gridLayout.addWidget(table)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(groupbox)
        self.verticalLayout.insertLayout(1, layout)

        warningImage = QtGui.QPixmap(":/warning.png").scaled(20, 20, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

        for i, warning in enumerate(warnings):
            table.insertRow(i)

            item = QtGui.QTableWidgetItem()
            item.setData(QtCore.Qt.DecorationRole, warningImage)
            table.setItem(i, 0, item)

            item = QtGui.QTableWidgetItem(warning)
            table.setItem(i, 1, item)

    def _readAutoCloseSetting(self):
        settings = settings_store.SettingsStore()
        settings.beginGroup(EpubGeneration._SETTINGS_GROUP)
        autoCloseValue = settings.value(EpubGeneration._AUTO_CLOSE_DIALOG_SETTING, False, bool)
        settings.endGroup()

        self.closeDialogInput.setCheckState(QtCore.Qt.Checked if autoCloseValue else QtCore.Qt.Unchecked)

    def _writeAutoCloseSetting(self):
        settings = settings_store.SettingsStore()
        settings.beginGroup(EpubGeneration._SETTINGS_GROUP)
        settings.setValue(EpubGeneration._AUTO_CLOSE_DIALOG_SETTING, self.closeDialogInput.isChecked())
        settings.endGroup()

    def _extendUi(self):
        movie = QtGui.QMovie(":/waiting.gif")
        self.imageLabel.setMovie(movie)
        movie.start()

        self.setFixedSize(self.width(), self.height())