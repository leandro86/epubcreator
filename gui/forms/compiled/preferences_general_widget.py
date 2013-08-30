# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'L:/Proyectos/python/epubcreator/gui\forms\preferences_general_widget.ui'
#
# Created: Fri Aug 30 00:44:30 2013
#      by: PyQt4 UI code generator 4.10.2
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

class Ui_GeneralPreferences(object):
    def setupUi(self, GeneralPreferences):
        GeneralPreferences.setObjectName(_fromUtf8("GeneralPreferences"))
        GeneralPreferences.resize(431, 254)
        self.gridLayout = QtGui.QGridLayout(GeneralPreferences)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.sigilPathInput = QtGui.QLineEdit(GeneralPreferences)
        self.sigilPathInput.setObjectName(_fromUtf8("sigilPathInput"))
        self.gridLayout.addWidget(self.sigilPathInput, 1, 1, 1, 1)
        self.changeSigilPathButton = QtGui.QPushButton(GeneralPreferences)
        self.changeSigilPathButton.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/preferences_general_widget/resources/images/search_16x16.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.changeSigilPathButton.setIcon(icon)
        self.changeSigilPathButton.setObjectName(_fromUtf8("changeSigilPathButton"))
        self.gridLayout.addWidget(self.changeSigilPathButton, 1, 2, 1, 1)
        self.label_9 = QtGui.QLabel(GeneralPreferences)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)
        self.editorInput = QtGui.QLineEdit(GeneralPreferences)
        self.editorInput.setObjectName(_fromUtf8("editorInput"))
        self.gridLayout.addWidget(self.editorInput, 0, 1, 1, 1)
        self.label_10 = QtGui.QLabel(GeneralPreferences)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 1)

        self.retranslateUi(GeneralPreferences)
        QtCore.QMetaObject.connectSlotsByName(GeneralPreferences)
        GeneralPreferences.setTabOrder(self.editorInput, self.sigilPathInput)
        GeneralPreferences.setTabOrder(self.sigilPathInput, self.changeSigilPathButton)

    def retranslateUi(self, GeneralPreferences):
        GeneralPreferences.setWindowTitle(_translate("GeneralPreferences", "Form", None))
        self.label_9.setText(_translate("GeneralPreferences", "Editor", None))
        self.label_10.setText(_translate("GeneralPreferences", "Ruta de Sigil", None))

from . import preferences_general_widget_rc
