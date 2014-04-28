from PyQt4 import QtCore, Qt, QtGui


class ExtendedQLabel(QtGui.QLabel):
    """
    Un QLabel con los siguientes añadidos:
        - Emite la señal "clicked" cuando se realiza click sobre él.
        - Emite la señal "entered" cuando recibe el foco del mouse.
        - Emite la señal "left" cuando pierde el foco del mouse.
    """

    clicked = Qt.pyqtSignal()
    entered = Qt.pyqtSignal()
    left = Qt.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def mouseReleaseEvent(self, event):
        self.clicked.emit()

    def enterEvent(self, event):
        self.entered.emit()

    def leaveEvent(self, event):
        self.left.emit()


class ExtendedQListWidget(QtGui.QListWidget):
    """
    Un QListWidget que emite la señal "deleteKeyPressed" cuando se presiona la tecla "delete".
    """

    deleteKeyPressed = Qt.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            self.deleteKeyPressed.emit()