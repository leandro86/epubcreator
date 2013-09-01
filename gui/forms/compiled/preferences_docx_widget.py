# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'L:/Proyectos/python/epubcreator/gui\forms\preferences_docx_widget.ui'
#
# Created: Sun Sep  1 19:23:37 2013
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

class Ui_DocxPreferences(object):
    def setupUi(self, DocxPreferences):
        DocxPreferences.setObjectName(_fromUtf8("DocxPreferences"))
        DocxPreferences.resize(695, 659)
        self.gridLayout = QtGui.QGridLayout(DocxPreferences)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.ignoreEmptyParagraphsInput = QtGui.QCheckBox(DocxPreferences)
        self.ignoreEmptyParagraphsInput.setObjectName(_fromUtf8("ignoreEmptyParagraphsInput"))
        self.gridLayout.addWidget(self.ignoreEmptyParagraphsInput, 0, 0, 1, 1)

        self.retranslateUi(DocxPreferences)
        QtCore.QMetaObject.connectSlotsByName(DocxPreferences)

    def retranslateUi(self, DocxPreferences):
        DocxPreferences.setWindowTitle(_translate("DocxPreferences", "Form", None))
        self.ignoreEmptyParagraphsInput.setToolTip(_translate("DocxPreferences", "Indica si los párrafos en blanco deben ignorarse, o reemplazarse por la \n"
"clase \"salto\" de acuerdo al siguiente criterio:\n"
"\n"
"Un párrafo en blanco, se reemplaza por la clase \"salto10\".\n"
"Dos o más, por la clase \"salto25\".", None))
        self.ignoreEmptyParagraphsInput.setText(_translate("DocxPreferences", "Ignorar Párrafos en Blanco", None))

