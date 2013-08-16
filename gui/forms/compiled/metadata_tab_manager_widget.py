# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'L:/Proyectos/python/epubcreator/gui\forms\metadata_tab_manager_widget.ui'
#
# Created: Thu Aug 15 22:19:09 2013
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

class Ui_MetadataTabManager(object):
    def setupUi(self, MetadataTabManager):
        MetadataTabManager.setObjectName(_fromUtf8("MetadataTabManager"))
        MetadataTabManager.resize(917, 718)
        self.horizontalLayout = QtGui.QHBoxLayout(MetadataTabManager)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.metadataTabManager = QtGui.QTabWidget(MetadataTabManager)
        self.metadataTabManager.setDocumentMode(False)
        self.metadataTabManager.setObjectName(_fromUtf8("metadataTabManager"))
        self.basicMetadata = BasicMetadata()
        self.basicMetadata.setObjectName(_fromUtf8("basicMetadata"))
        self.metadataTabManager.addTab(self.basicMetadata, _fromUtf8(""))
        self.additionalMetadata = AdditionalMetadata()
        self.additionalMetadata.setObjectName(_fromUtf8("additionalMetadata"))
        self.metadataTabManager.addTab(self.additionalMetadata, _fromUtf8(""))
        self.authorMetadata = AuthorMetadata()
        self.authorMetadata.setObjectName(_fromUtf8("authorMetadata"))
        self.metadataTabManager.addTab(self.authorMetadata, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.metadataTabManager)

        self.retranslateUi(MetadataTabManager)
        self.metadataTabManager.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MetadataTabManager)

    def retranslateUi(self, MetadataTabManager):
        MetadataTabManager.setWindowTitle(_translate("MetadataTabManager", "Form", None))
        self.metadataTabManager.setTabText(self.metadataTabManager.indexOf(self.basicMetadata), _translate("MetadataTabManager", "Datos Básicos", None))
        self.metadataTabManager.setTabText(self.metadataTabManager.indexOf(self.additionalMetadata), _translate("MetadataTabManager", "Datos Adicionales", None))
        self.metadataTabManager.setTabText(self.metadataTabManager.indexOf(self.authorMetadata), _translate("MetadataTabManager", "Datos del Autor", None))

from gui.metadata_tabs import AuthorMetadata, AdditionalMetadata, BasicMetadata
