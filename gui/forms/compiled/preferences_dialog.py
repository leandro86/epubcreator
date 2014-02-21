# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'L:/Proyectos/python/projects/epubcreator/src/gui\forms\preferences_dialog.ui'
#
# Created: Fri Feb 21 17:14:51 2014
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_Preferences(object):
    def setupUi(self, Preferences):
        Preferences.setObjectName(_fromUtf8("Preferences"))
        Preferences.resize(561, 357)
        self.verticalLayout = QtGui.QVBoxLayout(Preferences)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.listWidget = QtGui.QListWidget(Preferences)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        self.horizontalLayout_2.addWidget(self.listWidget)
        self.stackedPreferences = QtGui.QStackedWidget(Preferences)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedPreferences.sizePolicy().hasHeightForWidth())
        self.stackedPreferences.setSizePolicy(sizePolicy)
        self.stackedPreferences.setObjectName(_fromUtf8("stackedPreferences"))
        self.page_9 = GeneralPreferences()
        self.page_9.setObjectName(_fromUtf8("page_9"))
        self.stackedPreferences.addWidget(self.page_9)
        self.page_10 = DocxPreferences()
        self.page_10.setObjectName(_fromUtf8("page_10"))
        self.stackedPreferences.addWidget(self.page_10)
        self.horizontalLayout_2.addWidget(self.stackedPreferences)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtGui.QDialogButtonBox(Preferences)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Preferences)
        self.listWidget.setCurrentRow(0)
        self.stackedPreferences.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Preferences.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Preferences.reject)
        QtCore.QObject.connect(self.listWidget, QtCore.SIGNAL(_fromUtf8("currentRowChanged(int)")), self.stackedPreferences.setCurrentIndex)
        QtCore.QMetaObject.connectSlotsByName(Preferences)
        Preferences.setTabOrder(self.listWidget, self.buttonBox)

    def retranslateUi(self, Preferences):
        Preferences.setWindowTitle(_translate("Preferences", "Preferencias", None))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("Preferences", "Preferencias Generales", None))
        item = self.listWidget.item(1)
        item.setText(_translate("Preferences", "Conversión Docx", None))
        self.listWidget.setSortingEnabled(__sortingEnabled)

from gui.preferences_widgets import GeneralPreferences, DocxPreferences
