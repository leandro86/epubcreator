import collections

from PyQt4 import QtGui, QtCore


class LogWindow(QtGui.QDockWidget):
    def __init__(self, parent=None):
        super().__init__("Log de Conversión", parent)
        self.setObjectName("logWindow")

        self._logTable = QtGui.QTableWidget(self)

        self._setupTable()
        self.setWidget(self._logTable)

    def addlogMessages(self, logMessages):
        self._logTable.clear()

        if not logMessages:
            self._displayNoProblemsMessage()
            return

        self._configureTableForResults()

        distinctLogMessages = collections.Counter([logMessage.message for logMessage in logMessages])
        for i, msg in enumerate(distinctLogMessages.items()):
            self._logTable.insertRow(self._logTable.rowCount())

            # Por ahora asumo que si hay mensajes, son de warning
            item = QtGui.QTableWidgetItem()
            item.setIcon(self.style().standardIcon(QtGui.QStyle.SP_MessageBoxWarning))
            self._logTable.setItem(i, 0, item)

            item = QtGui.QTableWidgetItem(msg[0])
            self._logTable.setItem(i, 1, item)

            item = QtGui.QTableWidgetItem(str(msg[1]))
            self._logTable.setItem(i, 2, item)

        self._logTable.resizeColumnToContents(0)
        self._logTable.resizeColumnToContents(1)
        self._logTable.resizeColumnToContents(2)
        #self._logTable.resizeRowToContents(1)

    def _setupTable(self):
        self._logTable.horizontalHeader().setStretchLastSection(True)
        self._logTable.setTabKeyNavigation(False)
        self._logTable.setDropIndicatorShown(False)
        self._logTable.verticalHeader().setVisible(False)
        self._logTable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

    def _configureTableForResults(self):
        self._logTable.setRowCount(0)
        self._logTable.setColumnCount(3)
        self._logTable.setHorizontalHeaderLabels(("", "Descripción", "Ocurrencias"))
        self._logTable.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)

    def _displayNoProblemsMessage(self):
        self._logTable.setRowCount(1)
        self._logTable.setColumnCount(1)
        self._logTable.setHorizontalHeaderLabels(("Descripción",))
        item = QtGui.QTableWidgetItem("Conversión realizada con éxito.")
        item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        font = item.font()
        font.setPointSize(16)
        item.setFont(font)
        self._logTable.setItem(0, 0, item)
        self._logTable.resizeRowToContents(0)