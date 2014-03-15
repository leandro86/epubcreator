import datetime

from PyQt4 import QtGui, QtCore

from misc import language, utils
from gui.forms.compiled import basic_metadata_widget, additional_metadata_widget, author_metadata_widget
from epubcreator import ebook_metadata
from epubcreator.misc import epub_base_misc


class BasicMetadata(QtGui.QWidget, basic_metadata_widget.Ui_BasicMetadata):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Necesito guardarme los bytes de la imagen. Si obtengo los bytes directamente del qlabel, al hacer un
        # qlabel.pixmap().save() no obtengo exactamente los mismos bytes, ya que debo especificar el formato
        # al guardar la imagen, y dependiendo del tipo de compresión y demás, no obtengo los bytes originales. Esto
        # es obviamente un problema cuando el usuario especificó que no quiere que se haga ningún procesamiento a
        # las imágenes.
        # Una posibilidad era convertir el QPixmap en QImage, y de ahí obtener los bytes, pero no es nada fácil, ya
        # desde el QImage solamente puedo obtener un puntero hacia el primer byte, y de allí en más debo ir
        # iterando por todos los bytes, teniendo en cuenta el formato de la imagen y cómo están alineados los bytes.
        self._coverImageBytes = None

        self._populateCoverModificationOptions()
        self._connectSignals()

    def getTitle(self):
        return self.titleInput.text().strip()

    def getSubtitle(self):
        return self.subtitleInput.text().strip()

    def getAuthors(self):
        """
        Retorna los autores ingresados por el usuario.

        @return: una lista de Person.
        """
        authors = []

        for i in range(self.authorsList.count()):
            person = self.authorsList.item(i).data(QtCore.Qt.UserRole)
            authors.append(person)

        return authors

    def getCoverModification(self):
        return self.coverModificationInput.currentText().strip()

    def getCoverDesigner(self):
        return self.coverDesignerInput.text().strip()

    def getSynopsis(self):
        return self.synopsisInput.toPlainText().strip()

    def getCoverImage(self):
        """
        Retorna la imagen de portada.

        @return: los bytes de la imagen.
        """
        return self._coverImageBytes

    def _populateCoverModificationOptions(self):
        for i, option in enumerate(epub_base_misc.CoverModification.getOptions()):
            self.coverModificationInput.addItem(option[0])
            self.coverModificationInput.setItemData(i, option[1], QtCore.Qt.ToolTipRole)

    def _changeCoverImage(self):
        imageName = QtGui.QFileDialog.getOpenFileName(self, "Seleccionar Imagen",
                                                      "L:\\libros\\epubcreator_tests", "Imágenes (*.jpg)")
        if imageName:
            with open(imageName, "rb") as file:
                self._coverImageBytes = file.read()

            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(self._coverImageBytes)
            self.coverImage.setPixmap(pixmap)

    def _addAuthorToList(self):
        name = self.authorInput.text().strip()
        fileAs = self.authorFileAsInput.text().strip()

        if name:
            # Compruebo que el nombre del autor no haya sido agregado ya a la lista
            for i in range(self.authorsList.count()):
                if self.authorsList.item(i).data(QtCore.Qt.UserRole).name == name:
                    return

            item = QtGui.QListWidgetItem("{0} --> {1}".format(name, fileAs))
            item.setData(QtCore.Qt.UserRole, ebook_metadata.Person(name, fileAs))
            self.authorsList.addItem(item)

    def _removeSelectedAuthorFromList(self):
        if self.authorsList.currentItem() is not None:
            self.authorsList.takeItem(self.authorsList.row(self.authorsList.currentItem()))

    def _populateCurrentAuthorData(self, selectedAuthor):
        if selectedAuthor is None:
            return

        person = selectedAuthor.data(QtCore.Qt.UserRole)
        self.authorInput.setText(person.name)
        self.authorFileAsInput.setText(person.fileAs)

    def _updateAuthorFileAs(self, authorName):
        self.authorFileAsInput.setText(utils.Utilities.orderByLastName(authorName.strip()))

    def _authorInputKeyPressed(self, event):
        print(event)

    def _connectSignals(self):
        self.coverImage.clicked.connect(self._changeCoverImage)

        self.addAuthorButton.clicked.connect(self._addAuthorToList)
        self.authorsList.deleteKeyPressed.connect(self._removeSelectedAuthorFromList)
        self.authorsList.currentItemChanged.connect(self._populateCurrentAuthorData)
        self.authorInput.textChanged.connect(self._updateAuthorFileAs)
        self.authorInput.returnPressed.connect(self._addAuthorToList)


class AdditionalMetadata(QtGui.QWidget, additional_metadata_widget.Ui_AdditionalMetadata):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self._populateLanguages()
        self._populateGenreTypes()
        self._populateGenresAndSubGenres()

        self.collectionVolumeInput.setEnabled(False)

        # Por defecto, el combobox del lenguaje muestra "español"
        self.languageInput.setCurrentIndex(self.languageInput.findText(language.Language.getLanguageName("es")))

        self._connectSignals()

    def getOriginalTitle(self):
        return self.originalTitleInput.text().strip()

    def getPublicationDate(self):
        """
        Retorna la fecha de publicación.

        @return: un date.

        @raise: ValidationException, si la fecha no tiene un formato válido.
        """
        if self.publicationDateInput.text() != "--":
            try:
                return datetime.datetime.strptime(self.publicationDateInput.text().strip(), "%d-%m-%Y").date()
            except ValueError:
                raise ValidationException("Fecha de publicación no válida", "El formato de la fecha de publicación "
                                                                            "debe ser: dd-mm-aaaa. Si no conoce el "
                                                                            "día o mes exacto, coloque el 1 de enero.",
                                          self, self.publicationDateInput)

    def getLanguageCode(self):
        return language.Language.getLanguageCode(self.languageInput.currentText())

    def getTranslators(self):
        """
        Retorna los traductores ingresados por el usuario.

        @return: una lista de Person.
        """
        translators = []

        for i in range(self.translatorsList.count()):
            person = self.translatorsList.item(i).data(QtCore.Qt.UserRole)
            translators.append(person)

        return translators

    def getIlustrators(self):
        """
        Retorna los ilustradores ingresados por el usuario.

        @return: una lista de Person.
        """
        ilustrators = []

        for i in range(self.ilustratorsList.count()):
            person = self.ilustratorsList.item(i).data(QtCore.Qt.UserRole)
            ilustrators.append(person)

        return ilustrators

    def getGenres(self):
        """
        Retorna los géneros ingresados por el usuario.

        @return: una lista de Genre.
        """
        genres = []

        for i in range(self.genresList.count()):
            genre = self.genresList.item(i).data(QtCore.Qt.UserRole)
            genres.append(genre)

        return genres

    def getCollection(self):
        """
        Retorna la saga, serie y volumen.

        @return: una tupla de strings con: saga, serie, volumen.

        @raise: ValidationException, si se especificó una saga pero no una serie, o si se especificó
                una serie pero no el número de volumen.
        """
        collectionName = self.collectionNameInput.text().strip()
        subCollectionName = self.subCollectionNameInput.text().strip()
        collectionVolume = self.collectionVolumeInput.text().strip()

        if collectionName and not subCollectionName:
            raise ValidationException("No se especificó serie",
                                      "Se especificó el nombre de la saga, pero no la serie.",
                                      self,
                                      self.subCollectionNameInput)
        elif subCollectionName and not collectionVolume:
            raise ValidationException("No se especificó volumen de la serie",
                                      "Se especificó un nombre para la serie, pero no el número de volumen.",
                                      self,
                                      self.collectionVolumeInput)
        else:
            return collectionName, subCollectionName, collectionVolume

    def _populateLanguages(self):
        for languageName in language.Language.getSortedLanguagesNames():
            self.languageInput.addItem(languageName)

    def _populateGenreTypes(self):
        for genreType in epub_base_misc.Genre.getTypes():
            self.genreTypeInput.addItem(genreType)

    def _populateGenresAndSubGenres(self):
        selectedGenreType = self.genreTypeInput.currentText()
        genres = epub_base_misc.Genre.getGenres(selectedGenreType)
        subGenres = epub_base_misc.Genre.getSubGenres(selectedGenreType)

        self.genreGenreInput.clear()
        self.genreSubGenreInput.clear()

        for i, genre in enumerate(genres):
            self.genreGenreInput.addItem(genre[0])
            self.genreGenreInput.setItemData(i, genre[1], QtCore.Qt.ToolTipRole)

        for i, subGenre in enumerate(subGenres):
            self.genreSubGenreInput.addItem(subGenre[0])
            self.genreSubGenreInput.setItemData(i, subGenre[1], QtCore.Qt.ToolTipRole)

    def _addTranslatorToList(self):
        name = self.translatorInput.text().strip()
        fileAs = self.translatorFileAsInput.text().strip()

        if name:
            self._addPersonToList(self.translatorsList, name, fileAs)

    def _removeCurrentItemFromList(self):
        listWidget = self.sender()
        if listWidget.currentItem() is not None:
            listWidget.takeItem(listWidget.row(listWidget.currentItem()))

    def _populateCurrentTranslatorData(self, selectedTranslator):
        if selectedTranslator is None:
            return

        person = selectedTranslator.data(QtCore.Qt.UserRole)
        self.translatorInput.setText(person.name)
        self.translatorFileAsInput.setText(person.fileAs)

    def _updateTranslatorFileAs(self, translatorName):
        self.translatorFileAsInput.setText(utils.Utilities.orderByLastName(translatorName.strip()))

    def _addIlustratorToList(self):
        name = self.ilustratorInput.text().strip()
        fileAs = self.ilustratorFileAsInput.text().strip()

        if name:
            self._addPersonToList(self.ilustratorsList, name, fileAs)

    def _populateCurrentIlustratorData(self, selectedIlustrator):
        if selectedIlustrator is None:
            return

        person = selectedIlustrator.data(QtCore.Qt.UserRole)
        self.ilustratorInput.setText(person.name)
        self.ilustratorFileAsInput.setText(person.fileAs)

    def _updateIlustratorFileAs(self, ilustratorName):
        self.ilustratorFileAsInput.setText(utils.Utilities.orderByLastName(ilustratorName.strip()))

    def _addGenreToList(self):
        genreType = self.genreTypeInput.currentText()
        genreGenre = self.genreGenreInput.currentText()
        genreSubGenre = self.genreSubGenreInput.currentText()

        item = QtGui.QListWidgetItem("{0}, {1}, {2}".format(genreType, genreGenre, genreSubGenre))

        # Compruebo que el género no haya sido agregado ya a la lista
        for i in range(self.genresList.count()):
            if self.genresList.item(i).text() == item.text():
                return

        item.setData(QtCore.Qt.UserRole, ebook_metadata.Genre(genreType, genreGenre, genreSubGenre))
        self.genresList.addItem(item)

        self.genresList.sortItems()

    def _addPersonToList(self, listWidget, name, fileAs):
        item = QtGui.QListWidgetItem("{0} --> {1}".format(name, fileAs))

        # Compruebo que el nombre de la persona no haya sido agregado ya a la lista
        for i in range(listWidget.count()):
            if listWidget.item(i).data(QtCore.Qt.UserRole).name == name:
                return

        item.setData(QtCore.Qt.UserRole, ebook_metadata.Person(name, fileAs))
        listWidget.addItem(item)

    def _connectSignals(self):
        self.addGenreButton.clicked.connect(self._addGenreToList)
        self.genreTypeInput.currentIndexChanged.connect(self._populateGenresAndSubGenres)
        self.genresList.deleteKeyPressed.connect(self._removeCurrentItemFromList)

        self.subCollectionNameInput.textChanged.connect(
            lambda s: self.collectionVolumeInput.setEnabled(len(s.strip()) != 0))

        self.addTranslatorButton.clicked.connect(self._addTranslatorToList)
        self.translatorsList.deleteKeyPressed.connect(self._removeCurrentItemFromList)
        self.translatorsList.currentItemChanged.connect(self._populateCurrentTranslatorData)
        self.translatorInput.textChanged.connect(self._updateTranslatorFileAs)
        self.translatorInput.returnPressed.connect(self._addTranslatorToList)

        self.addIlustratorButton.clicked.connect(self._addIlustratorToList)
        self.ilustratorsList.deleteKeyPressed.connect(self._removeCurrentItemFromList)
        self.ilustratorsList.currentItemChanged.connect(self._populateCurrentIlustratorData)
        self.ilustratorInput.textChanged.connect(self._updateIlustratorFileAs)
        self.ilustratorInput.returnPressed.connect(self._addIlustratorToList)


class AuthorMetadata(QtGui.QWidget, author_metadata_widget.Ui_AuthorMetadata):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Debo guardarme aparte los bytes de la imagen, ya no me sirve a mí obtenerlos desde el QLabel
        # directamente (mismo problema que con la imagen de portada...)
        self._authorImageBytes = None

        self.authorImage.clicked.connect(self._changeAuthorImage)

    def getDedication(self):
        return self.authorDedicationInput.toPlainText().strip()

    def getImage(self):
        """
        Retorna la imagen del autor.

        @return: los bytes de la imagen.
        """
        return self._authorImageBytes

    def getBiography(self):
        return self.authorBiographyInput.toPlainText().strip()

    def _changeAuthorImage(self):
        imageName = QtGui.QFileDialog.getOpenFileName(self, "Seleccionar Imagen",
                                                      "L:\\libros\\epubcreator_tests", "Imágenes (*.jpg)")
        if imageName:
            with open(imageName, "rb") as file:
                self._authorImageBytes = file.read()

            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(self._authorImageBytes)
            self.authorImage.setPixmap(pixmap)


class ValidationException(Exception):
    def __init__(self, error, description, tab, widget):
        self.error = error
        self.description = description
        self.tab = tab
        self.widget = widget