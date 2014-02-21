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