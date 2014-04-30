from PyQt4 import QtGui

from epubcreator.gui.forms import author_data_edit_dialog_ui
from epubcreator.gui import image_edit
from epubcreator.epubbase import images, ebook_metadata
from epubcreator.misc import gui_utils, settings_store


class AuthorDataEdit(QtGui.QDialog, author_data_edit_dialog_ui.Ui_Dialog):
    _GENDERS_TO_TEXT = {ebook_metadata.Person.MALE_GENDER: "Autor",
                        ebook_metadata.Person.FEMALE_GENDER: "Autora"}

    _TEXT_TO_GENDERS = {"Autor": ebook_metadata.Person.MALE_GENDER,
                        "Autora": ebook_metadata.Person.FEMALE_GENDER}

    def __init__(self, author, canChooseGender=False, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._extendUi(canChooseGender)

        self._author = author

        self._populateData()
        self._connectSignals()

    def _populateData(self):
        self.authorBiographyInput.setPlainText(self._author.biography)
        self._changeAuthorImage(self._author.image)
        self.authorGenderInput.setCurrentIndex(self.authorGenderInput.findText(AuthorDataEdit._GENDERS_TO_TEXT[self._author.gender]))

    def _openImageSelectionDialog(self):
        imgFilter = "Imágenes ({0})".format(" ".join(("*.{0}".format(f[0]) for f in images.AuthorImage.SUPPORTED_FORMATS if not f[1])))
        imageName = QtGui.QFileDialog.getOpenFileName(self, "Seleccionar Imagen", filter=imgFilter)

        if imageName:
            settings = settings_store.SettingsStore()

            try:
                image = images.AuthorImage(imageName, allowProcessing=settings.allowImageProcessing)
            except images.InvalidDimensionsError:
                gui_utils.displayStdErrorDialog("La imagen de autor seleccionada no tiene las dimensiones requeridas, que deben ser "
                                                "de {0}px de ancho y {1}px de alto. Si desea que la imagen se redimensione "
                                                "automáticamente, habilite la opción para permitir el procesamiento de las imágenes desde el "
                                                "menú Preferencias.".format(images.AuthorImage.WIDTH, images.AuthorImage.HEIGHT))
                return
            except images.MaxSizeExceededError:
                gui_utils.displayStdErrorDialog("La imagen de autor excede el tamaño máximo permitido, que debe "
                                                "ser menor o igual a {0} kB. Si desea que la calidad de la imagen se ajuste automáticamente para "
                                                "reducir su tamaño, habilite la opción para permitir el procesamiento de las imágenes desde "
                                                "el menú Preferencias.".format(images.AuthorImage.MAX_SIZE_IN_BYTES // 1000))
                return
            except images.ProgressiveImageError:
                gui_utils.displayStdErrorDialog("La imagen de autor no puede ser abierta porque fue guardada en modo progresivo. Guárdela de "
                                                "manera normal y vuelva a abrirla, o habilite la opción para permitir el procesamiento de las "
                                                "imágenes desde el menú Preferencias.")
                return

            self._author.image = image
            self._changeAuthorImage(image)

    def _saveAuthorBiography(self):
        self._author.biography = self.authorBiographyInput.toPlainText().strip()

    def _changeAuthorImage(self, authorImage):
        if authorImage:
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(authorImage.toBytes())
            self.authorImage.setPixmap(pixmap)

        self.ediAuthorImageButton.setEnabled(self._author.image is not None and settings_store.SettingsStore().allowImageProcessing)

    def _editAuthorImage(self):
        clonedAuthorImage = self._author.image

        if image_edit.ImageEdit(clonedAuthorImage, imageType=image_edit.ImageEdit.AUTHOR, parent=self).exec() == QtGui.QDialog.Accepted:
            self._author.image = clonedAuthorImage
            self._changeAuthorImage(clonedAuthorImage)

    def _saveAuthorGender(self, newGenderText):
        self._author.gender = AuthorDataEdit._TEXT_TO_GENDERS[newGenderText]

    def _extendUi(self, canChooseGender):
        for genderText in AuthorDataEdit._TEXT_TO_GENDERS:
            self.authorGenderInput.addItem(genderText)

        self.authorGenderInput.setEnabled(canChooseGender)

    def _connectSignals(self):
        self.authorImage.clicked.connect(self._openImageSelectionDialog)
        self.ediAuthorImageButton.clicked.connect(self._editAuthorImage)
        self.authorGenderInput.currentIndexChanged.connect(lambda index: self._saveAuthorGender(self.authorGenderInput.itemText(index)))

        # Guardo directamente el texto de la biografía cada vez que se realice un cambio en el control.
        self.authorBiographyInput.textChanged.connect(self._saveAuthorBiography)