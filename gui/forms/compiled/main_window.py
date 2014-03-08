# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'L:/Proyectos/python/projects/epubcreator/src/gui\forms\main_window.ui'
#
# Created by PyQt4 UI code generator
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(817, 656)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(6, 6, 6, 0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.metadataTabManager = MetadataTabManager(self.centralwidget)
        self.metadataTabManager.setObjectName(_fromUtf8("metadataTabManager"))
        self.horizontalLayout.addWidget(self.metadataTabManager)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 817, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuArchivo = QtGui.QMenu(self.menubar)
        self.menuArchivo.setObjectName(_fromUtf8("menuArchivo"))
        self.menuVer = QtGui.QMenu(self.menubar)
        self.menuVer.setObjectName(_fromUtf8("menuVer"))
        self.menuAyuda = QtGui.QMenu(self.menubar)
        self.menuAyuda.setObjectName(_fromUtf8("menuAyuda"))
        MainWindow.setMenuBar(self.menubar)
        self.openFileAction = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/main_window/resources/images/open_24x24.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.openFileAction.setIcon(icon)
        self.openFileAction.setObjectName(_fromUtf8("openFileAction"))
        self.generateEpubAction = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/main_window/resources/images/epub.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.generateEpubAction.setIcon(icon1)
        self.generateEpubAction.setObjectName(_fromUtf8("generateEpubAction"))
        self.preferencesAction = QtGui.QAction(MainWindow)
        self.preferencesAction.setMenuRole(QtGui.QAction.PreferencesRole)
        self.preferencesAction.setObjectName(_fromUtf8("preferencesAction"))
        self.quitAction = QtGui.QAction(MainWindow)
        self.quitAction.setMenuRole(QtGui.QAction.QuitRole)
        self.quitAction.setObjectName(_fromUtf8("quitAction"))
        self.toggleToolBarAction = QtGui.QAction(MainWindow)
        self.toggleToolBarAction.setCheckable(True)
        self.toggleToolBarAction.setObjectName(_fromUtf8("toggleToolBarAction"))
        self.toggleLogWindowAction = QtGui.QAction(MainWindow)
        self.toggleLogWindowAction.setCheckable(True)
        self.toggleLogWindowAction.setObjectName(_fromUtf8("toggleLogWindowAction"))
        self.aboutAction = QtGui.QAction(MainWindow)
        self.aboutAction.setMenuRole(QtGui.QAction.AboutRole)
        self.aboutAction.setObjectName(_fromUtf8("aboutAction"))
        self.toolBar.addAction(self.openFileAction)
        self.toolBar.addAction(self.generateEpubAction)
        self.menuArchivo.addAction(self.openFileAction)
        self.menuArchivo.addAction(self.generateEpubAction)
        self.menuArchivo.addSeparator()
        self.menuArchivo.addAction(self.preferencesAction)
        self.menuArchivo.addSeparator()
        self.menuArchivo.addAction(self.quitAction)
        self.menuVer.addAction(self.toggleToolBarAction)
        self.menuVer.addSeparator()
        self.menuVer.addAction(self.toggleLogWindowAction)
        self.menuAyuda.addAction(self.aboutAction)
        self.menubar.addAction(self.menuArchivo.menuAction())
        self.menubar.addAction(self.menuVer.menuAction())
        self.menubar.addAction(self.menuAyuda.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "Barra de Herramientas", None))
        self.menuArchivo.setTitle(_translate("MainWindow", "Archivo", None))
        self.menuVer.setTitle(_translate("MainWindow", "Ver", None))
        self.menuAyuda.setTitle(_translate("MainWindow", "Ayuda", None))
        self.openFileAction.setText(_translate("MainWindow", "Abrir", None))
        self.openFileAction.setToolTip(_translate("MainWindow", "Abrir Archivo", None))
        self.generateEpubAction.setText(_translate("MainWindow", "Generar ePub", None))
        self.preferencesAction.setText(_translate("MainWindow", "Preferencias", None))
        self.quitAction.setText(_translate("MainWindow", "Salir", None))
        self.toggleToolBarAction.setText(_translate("MainWindow", "Barra de Herramientas", None))
        self.toggleLogWindowAction.setText(_translate("MainWindow", "Log de Conversión", None))
        self.aboutAction.setText(_translate("MainWindow", "Acerca de...", None))

from gui.metadata_tab_manager import MetadataTabManager
from . import main_window_rc
