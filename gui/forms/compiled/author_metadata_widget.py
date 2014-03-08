# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'L:/Proyectos/python/projects/epubcreator/src/gui\forms\author_metadata_widget.ui'
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

class Ui_AuthorMetadata(object):
    def setupUi(self, AuthorMetadata):
        AuthorMetadata.setObjectName(_fromUtf8("AuthorMetadata"))
        AuthorMetadata.resize(681, 544)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AuthorMetadata.sizePolicy().hasHeightForWidth())
        AuthorMetadata.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QtGui.QGridLayout(AuthorMetadata)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label = QtGui.QLabel(AuthorMetadata)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.authorDedicationInput = QtGui.QPlainTextEdit(AuthorMetadata)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.authorDedicationInput.sizePolicy().hasHeightForWidth())
        self.authorDedicationInput.setSizePolicy(sizePolicy)
        self.authorDedicationInput.setMaximumSize(QtCore.QSize(16777215, 100))
        self.authorDedicationInput.setObjectName(_fromUtf8("authorDedicationInput"))
        self.gridLayout_2.addWidget(self.authorDedicationInput, 0, 1, 1, 2)
        self.label_2 = QtGui.QLabel(AuthorMetadata)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.frame = QtGui.QFrame(AuthorMetadata)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_5.setMargin(0)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.authorImage = ExtendedQLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.authorImage.sizePolicy().hasHeightForWidth())
        self.authorImage.setSizePolicy(sizePolicy)
        self.authorImage.setScaledContents(True)
        self.authorImage.setAlignment(QtCore.Qt.AlignCenter)
        self.authorImage.setWordWrap(True)
        self.authorImage.setObjectName(_fromUtf8("authorImage"))
        self.horizontalLayout_5.addWidget(self.authorImage)
        self.horizontalLayout_3.addWidget(self.frame)
        self.label_6 = QtGui.QLabel(AuthorMetadata)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_3.addWidget(self.label_6)
        self.authorBiographyInput = QtGui.QPlainTextEdit(AuthorMetadata)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.authorBiographyInput.sizePolicy().hasHeightForWidth())
        self.authorBiographyInput.setSizePolicy(sizePolicy)
        self.authorBiographyInput.setFrameShape(QtGui.QFrame.StyledPanel)
        self.authorBiographyInput.setObjectName(_fromUtf8("authorBiographyInput"))
        self.horizontalLayout_3.addWidget(self.authorBiographyInput)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(2, 1)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 1, 1, 1, 2)

        self.retranslateUi(AuthorMetadata)
        QtCore.QMetaObject.connectSlotsByName(AuthorMetadata)

    def retranslateUi(self, AuthorMetadata):
        AuthorMetadata.setWindowTitle(_translate("AuthorMetadata", "Form", None))
        self.label.setText(_translate("AuthorMetadata", "Dedicatoria", None))
        self.label_2.setText(_translate("AuthorMetadata", "Imagen", None))
        self.authorImage.setText(_translate("AuthorMetadata", "<html><head/><body><p><span style=\" text-decoration: underline; color:#0000ff;\">Haga click aquí para seleccionar la imagen del autor</span></p></body></html>", None))
        self.label_6.setText(_translate("AuthorMetadata", "Biografía", None))

from gui.custom_widgets import ExtendedQLabel
