# -*- coding: utf-8 -*-

# Copyright (C) 2013 Leandro
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4 import QtGui, QtCore

from ecreator import ebook_data
from gui.forms.compiled import metadata_tab_manager_widget
from gui import metadata_tabs


class MetadataTabManager(QtGui.QWidget, metadata_tab_manager_widget.Ui_MetadataTabManager):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Contiene un tag 'img' cuyo atributo 'src' es una imagen de un ícono de error
        self._errorImgTag = self._getErrorImgTag()

    def getEbookMetadata(self):
        """
        Retorna los metadatos ingresados por el usuario.

        @return: un objeto Metadata si no hubo errores, sino None.
        """
        metadata = ebook_data.Metadata()

        if (self._populateBasicMetadata(metadata) and
            self._populateAdditionalMetadata(metadata) and
            self._populateAuthorMetadata(metadata)):
            return metadata
        else:
            return None

    def _populateBasicMetadata(self, metadata):
        isValid = True

        metadata.coverImage = self.basicMetadata.getCoverImage()
        metadata.title = self.basicMetadata.getTitle()
        metadata.subtitle = self.basicMetadata.getSubtitle()
        metadata.synopsis = self.basicMetadata.getSynopsis()
        metadata.coverDesignOrTweak = self.basicMetadata.getCoverModification()
        metadata.coverDesigner = self.basicMetadata.getCoverDesigner()

        for author in self.basicMetadata.getAuthors():
            metadata.authors.append(author)

        return isValid

    def _populateAdditionalMetadata(self, metadata):
        isValid = True

        metadata.originalTitle = self.additionalMetadata.getOriginalTitle()

        try:
            metadata.publicationDate = self.additionalMetadata.getPublicationDate()
        except metadata_tabs.ValidationException as e:
            self._showError(e.error, e.description, e.tab, e.widget)
            isValid = False

        try:
            collection = self.additionalMetadata.getCollection()
            metadata.collectionName = collection[0]
            metadata.subCollectionName = collection[1]
            metadata.collectionVolume = collection[2]
        except metadata_tabs.ValidationException as e:
            self._showError(e.error, e.description, e.tab, e.widget)
            isValid = False

        metadata.language = self.additionalMetadata.getLanguageCode()
        metadata.publisher = self.additionalMetadata.getPublisher()

        for translator in self.additionalMetadata.getTranslators():
            metadata.translators.append(translator)

        for ilustrator in self.additionalMetadata.getIlustrators():
            metadata.ilustrators.append(ilustrator)

        for genre in self.additionalMetadata.getGenres():
            metadata.genres.append(genre)

        return isValid

    def _populateAuthorMetadata(self, metadata):
        isValid = True

        metadata.dedication = self.authorMetadata.getDedication()
        metadata.authorImage = self.authorMetadata.getImage()
        metadata.authorBiography = self.authorMetadata.getBiography()

        return isValid

    def _showError(self, error, description, tab, widget):
        toolTipMsg = ('<p>{0} <b> {1}</b></p>'
                      '<p style="margin-left: 0.5em;">{2}</p>'.format(self._errorImgTag, error, description))
        toolTipPos = widget.mapToGlobal(QtCore.QPoint(0, 0))

        self.metadataTabManager.setCurrentWidget(tab)
        widget.setFocus()

        QtGui.QToolTip.showText(toolTipPos, toolTipMsg)

    def _getErrorImgTag(self):
        """
        Retorna un tag 'img' cuyo source es el ícono de error y depende del sistema operativo.

        @return: un string con el tag img (cuyo atributo 'src' es la imagen codificada en base64).
        """
        # Html permite poner en 'src' datos codificados en base64. Esto me permite cargar a mí el ícono de error
        # estándar para cada operativo. Sino lo que tengo que hacer es meter algún ícono de error genérico en un
        # archivo de recurso y cargarlo.
        errorIcon = self.style().standardIcon(QtGui.QStyle.SP_MessageBoxCritical)

        ba = QtCore.QByteArray()
        buffer = QtCore.QBuffer(ba)
        buffer.open(QtCore.QIODevice.WriteOnly)
        errorIcon.pixmap(QtCore.QSize(24, 24)).save(buffer, "PNG")
        imgTag = '<img src="data:image/png;base64,{0}"/>'.format(bytes(buffer.data().toBase64()).decode("utf-8"))
        buffer.close()

        return imgTag