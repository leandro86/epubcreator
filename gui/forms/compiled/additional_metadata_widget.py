# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'additional_metadata_widget.ui'
#
# Created: Sat Mar 15 22:27:08 2014
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

class Ui_AdditionalMetadata(object):
    def setupUi(self, AdditionalMetadata):
        AdditionalMetadata.setObjectName(_fromUtf8("AdditionalMetadata"))
        AdditionalMetadata.resize(837, 594)
        AdditionalMetadata.setStyleSheet(_fromUtf8("QGroupBox\n"
"{ \n"
"    border: 1px solid #A6A6A6; \n"
"    border-radius: 5px; \n"
"}"))
        self.gridLayout = QtGui.QGridLayout(AdditionalMetadata)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.publicationDateInput = QtGui.QLineEdit(AdditionalMetadata)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.publicationDateInput.sizePolicy().hasHeightForWidth())
        self.publicationDateInput.setSizePolicy(sizePolicy)
        self.publicationDateInput.setMinimumSize(QtCore.QSize(0, 0))
        self.publicationDateInput.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.publicationDateInput.setObjectName(_fromUtf8("publicationDateInput"))
        self.gridLayout.addWidget(self.publicationDateInput, 0, 3, 1, 1)
        self.label_6 = QtGui.QLabel(AdditionalMetadata)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)
        self.label_4 = QtGui.QLabel(AdditionalMetadata)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.label_2 = QtGui.QLabel(AdditionalMetadata)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.originalTitleInput = QtGui.QLineEdit(AdditionalMetadata)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.originalTitleInput.sizePolicy().hasHeightForWidth())
        self.originalTitleInput.setSizePolicy(sizePolicy)
        self.originalTitleInput.setMinimumSize(QtCore.QSize(0, 0))
        self.originalTitleInput.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.originalTitleInput.setObjectName(_fromUtf8("originalTitleInput"))
        self.gridLayout.addWidget(self.originalTitleInput, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(AdditionalMetadata)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        self.label_5 = QtGui.QLabel(AdditionalMetadata)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.label_12 = QtGui.QLabel(AdditionalMetadata)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout.addWidget(self.label_12, 4, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(AdditionalMetadata)
        self.groupBox.setStyleSheet(_fromUtf8(""))
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_8 = QtGui.QLabel(self.groupBox)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_2.addWidget(self.label_8, 0, 0, 1, 1)
        self.translatorInput = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.translatorInput.sizePolicy().hasHeightForWidth())
        self.translatorInput.setSizePolicy(sizePolicy)
        self.translatorInput.setObjectName(_fromUtf8("translatorInput"))
        self.gridLayout_2.addWidget(self.translatorInput, 0, 1, 1, 1)
        self.translatorsList = ExtendedQListWidget(self.groupBox)
        self.translatorsList.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.translatorsList.sizePolicy().hasHeightForWidth())
        self.translatorsList.setSizePolicy(sizePolicy)
        self.translatorsList.setMinimumSize(QtCore.QSize(0, 0))
        self.translatorsList.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.translatorsList.setObjectName(_fromUtf8("translatorsList"))
        self.gridLayout_2.addWidget(self.translatorsList, 0, 2, 3, 1)
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 1, 0, 1, 1)
        self.translatorFileAsInput = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.translatorFileAsInput.sizePolicy().hasHeightForWidth())
        self.translatorFileAsInput.setSizePolicy(sizePolicy)
        self.translatorFileAsInput.setObjectName(_fromUtf8("translatorFileAsInput"))
        self.gridLayout_2.addWidget(self.translatorFileAsInput, 1, 1, 1, 1)
        self.addTranslatorButton = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addTranslatorButton.sizePolicy().hasHeightForWidth())
        self.addTranslatorButton.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/additional_metadata_widget/resources/images/add_16x16.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addTranslatorButton.setIcon(icon)
        self.addTranslatorButton.setIconSize(QtCore.QSize(16, 16))
        self.addTranslatorButton.setObjectName(_fromUtf8("addTranslatorButton"))
        self.gridLayout_2.addWidget(self.addTranslatorButton, 2, 0, 1, 2)
        self.gridLayout.addWidget(self.groupBox, 1, 1, 1, 3)
        self.groupBox_2 = QtGui.QGroupBox(AdditionalMetadata)
        self.groupBox_2.setTitle(_fromUtf8(""))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_9 = QtGui.QLabel(self.groupBox_2)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_3.addWidget(self.label_9, 0, 0, 1, 1)
        self.ilustratorInput = QtGui.QLineEdit(self.groupBox_2)
        self.ilustratorInput.setObjectName(_fromUtf8("ilustratorInput"))
        self.gridLayout_3.addWidget(self.ilustratorInput, 0, 1, 1, 1)
        self.ilustratorsList = ExtendedQListWidget(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ilustratorsList.sizePolicy().hasHeightForWidth())
        self.ilustratorsList.setSizePolicy(sizePolicy)
        self.ilustratorsList.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.ilustratorsList.setObjectName(_fromUtf8("ilustratorsList"))
        self.gridLayout_3.addWidget(self.ilustratorsList, 0, 2, 3, 1)
        self.label_10 = QtGui.QLabel(self.groupBox_2)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_3.addWidget(self.label_10, 1, 0, 1, 1)
        self.ilustratorFileAsInput = QtGui.QLineEdit(self.groupBox_2)
        self.ilustratorFileAsInput.setObjectName(_fromUtf8("ilustratorFileAsInput"))
        self.gridLayout_3.addWidget(self.ilustratorFileAsInput, 1, 1, 1, 1)
        self.addIlustratorButton = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addIlustratorButton.sizePolicy().hasHeightForWidth())
        self.addIlustratorButton.setSizePolicy(sizePolicy)
        self.addIlustratorButton.setIcon(icon)
        self.addIlustratorButton.setIconSize(QtCore.QSize(16, 16))
        self.addIlustratorButton.setObjectName(_fromUtf8("addIlustratorButton"))
        self.gridLayout_3.addWidget(self.addIlustratorButton, 2, 0, 1, 2)
        self.gridLayout.addWidget(self.groupBox_2, 2, 1, 1, 3)
        self.groupBox_3 = QtGui.QGroupBox(AdditionalMetadata)
        self.groupBox_3.setTitle(_fromUtf8(""))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_11 = QtGui.QLabel(self.groupBox_3)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_4.addWidget(self.label_11, 0, 0, 1, 1)
        self.genreTypeInput = QtGui.QComboBox(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.genreTypeInput.sizePolicy().hasHeightForWidth())
        self.genreTypeInput.setSizePolicy(sizePolicy)
        self.genreTypeInput.setObjectName(_fromUtf8("genreTypeInput"))
        self.gridLayout_4.addWidget(self.genreTypeInput, 0, 1, 1, 1)
        self.genresList = ExtendedQListWidget(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.genresList.sizePolicy().hasHeightForWidth())
        self.genresList.setSizePolicy(sizePolicy)
        self.genresList.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.genresList.setObjectName(_fromUtf8("genresList"))
        self.gridLayout_4.addWidget(self.genresList, 0, 2, 4, 1)
        self.label_14 = QtGui.QLabel(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout_4.addWidget(self.label_14, 1, 0, 1, 1)
        self.genreGenreInput = QtGui.QComboBox(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.genreGenreInput.sizePolicy().hasHeightForWidth())
        self.genreGenreInput.setSizePolicy(sizePolicy)
        self.genreGenreInput.setObjectName(_fromUtf8("genreGenreInput"))
        self.gridLayout_4.addWidget(self.genreGenreInput, 1, 1, 1, 1)
        self.label_15 = QtGui.QLabel(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.gridLayout_4.addWidget(self.label_15, 2, 0, 1, 1)
        self.genreSubGenreInput = QtGui.QComboBox(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.genreSubGenreInput.sizePolicy().hasHeightForWidth())
        self.genreSubGenreInput.setSizePolicy(sizePolicy)
        self.genreSubGenreInput.setObjectName(_fromUtf8("genreSubGenreInput"))
        self.gridLayout_4.addWidget(self.genreSubGenreInput, 2, 1, 1, 1)
        self.addGenreButton = QtGui.QPushButton(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addGenreButton.sizePolicy().hasHeightForWidth())
        self.addGenreButton.setSizePolicy(sizePolicy)
        self.addGenreButton.setIcon(icon)
        self.addGenreButton.setIconSize(QtCore.QSize(16, 16))
        self.addGenreButton.setObjectName(_fromUtf8("addGenreButton"))
        self.gridLayout_4.addWidget(self.addGenreButton, 3, 0, 1, 2)
        self.gridLayout.addWidget(self.groupBox_3, 3, 1, 1, 3)
        self.groupBox_4 = QtGui.QGroupBox(AdditionalMetadata)
        self.groupBox_4.setTitle(_fromUtf8(""))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.gridLayout_5 = QtGui.QGridLayout(self.groupBox_4)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.label_13 = QtGui.QLabel(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout_5.addWidget(self.label_13, 0, 2, 1, 1)
        self.subCollectionNameInput = QtGui.QLineEdit(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subCollectionNameInput.sizePolicy().hasHeightForWidth())
        self.subCollectionNameInput.setSizePolicy(sizePolicy)
        self.subCollectionNameInput.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.subCollectionNameInput.setObjectName(_fromUtf8("subCollectionNameInput"))
        self.gridLayout_5.addWidget(self.subCollectionNameInput, 0, 3, 1, 1)
        self.label_16 = QtGui.QLabel(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.gridLayout_5.addWidget(self.label_16, 0, 4, 1, 1)
        self.collectionVolumeInput = QtGui.QLineEdit(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.collectionVolumeInput.sizePolicy().hasHeightForWidth())
        self.collectionVolumeInput.setSizePolicy(sizePolicy)
        self.collectionVolumeInput.setMaximumSize(QtCore.QSize(50, 16777215))
        self.collectionVolumeInput.setObjectName(_fromUtf8("collectionVolumeInput"))
        self.gridLayout_5.addWidget(self.collectionVolumeInput, 0, 5, 1, 1)
        self.label_18 = QtGui.QLabel(self.groupBox_4)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.gridLayout_5.addWidget(self.label_18, 0, 0, 1, 1)
        self.collectionNameInput = QtGui.QLineEdit(self.groupBox_4)
        self.collectionNameInput.setObjectName(_fromUtf8("collectionNameInput"))
        self.gridLayout_5.addWidget(self.collectionNameInput, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox_4, 4, 1, 1, 3)

        self.retranslateUi(AdditionalMetadata)
        QtCore.QMetaObject.connectSlotsByName(AdditionalMetadata)
        AdditionalMetadata.setTabOrder(self.originalTitleInput, self.publicationDateInput)
        AdditionalMetadata.setTabOrder(self.publicationDateInput, self.translatorInput)
        AdditionalMetadata.setTabOrder(self.translatorInput, self.translatorFileAsInput)
        AdditionalMetadata.setTabOrder(self.translatorFileAsInput, self.addTranslatorButton)
        AdditionalMetadata.setTabOrder(self.addTranslatorButton, self.translatorsList)
        AdditionalMetadata.setTabOrder(self.translatorsList, self.ilustratorInput)
        AdditionalMetadata.setTabOrder(self.ilustratorInput, self.ilustratorFileAsInput)
        AdditionalMetadata.setTabOrder(self.ilustratorFileAsInput, self.addIlustratorButton)
        AdditionalMetadata.setTabOrder(self.addIlustratorButton, self.ilustratorsList)
        AdditionalMetadata.setTabOrder(self.ilustratorsList, self.genreTypeInput)
        AdditionalMetadata.setTabOrder(self.genreTypeInput, self.genreGenreInput)
        AdditionalMetadata.setTabOrder(self.genreGenreInput, self.genreSubGenreInput)
        AdditionalMetadata.setTabOrder(self.genreSubGenreInput, self.addGenreButton)
        AdditionalMetadata.setTabOrder(self.addGenreButton, self.genresList)
        AdditionalMetadata.setTabOrder(self.genresList, self.collectionNameInput)
        AdditionalMetadata.setTabOrder(self.collectionNameInput, self.subCollectionNameInput)
        AdditionalMetadata.setTabOrder(self.subCollectionNameInput, self.collectionVolumeInput)

    def retranslateUi(self, AdditionalMetadata):
        AdditionalMetadata.setWindowTitle(_translate("AdditionalMetadata", "Form", None))
        self.publicationDateInput.setInputMask(_translate("AdditionalMetadata", "00-00-0000; ", None))
        self.label_6.setText(_translate("AdditionalMetadata", "Géneros", None))
        self.label_4.setText(_translate("AdditionalMetadata", "Traductores", None))
        self.label_2.setText(_translate("AdditionalMetadata", "Título original", None))
        self.label_3.setText(_translate("AdditionalMetadata", "Fecha de publicación", None))
        self.label_5.setText(_translate("AdditionalMetadata", "Ilustradores", None))
        self.label_12.setText(_translate("AdditionalMetadata", "Colección", None))
        self.label_8.setText(_translate("AdditionalMetadata", "Nombre", None))
        self.label_7.setText(_translate("AdditionalMetadata", "Mostrar como", None))
        self.addTranslatorButton.setText(_translate("AdditionalMetadata", "Agregar Traductor", None))
        self.label_9.setText(_translate("AdditionalMetadata", "Nombre", None))
        self.label_10.setText(_translate("AdditionalMetadata", "Mostrar como", None))
        self.addIlustratorButton.setText(_translate("AdditionalMetadata", "Agregar Ilustrador", None))
        self.label_11.setText(_translate("AdditionalMetadata", "Tipo", None))
        self.label_14.setText(_translate("AdditionalMetadata", "Género", None))
        self.label_15.setText(_translate("AdditionalMetadata", "Subgénero", None))
        self.addGenreButton.setText(_translate("AdditionalMetadata", "Agregar Género", None))
        self.label_13.setText(_translate("AdditionalMetadata", "Serie", None))
        self.label_16.setText(_translate("AdditionalMetadata", "Volumen", None))
        self.label_18.setText(_translate("AdditionalMetadata", "Saga", None))

from gui.custom_widgets import ExtendedQListWidget
from . import additional_metadata_widget_rc
