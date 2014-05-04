import os

from PyQt4 import QtCore, QtGui

from epubcreator.epubbase.ebook import Ebook
from epubcreator.converters.converter_factory import ConverterFactory


class SettingsStore(QtCore.QSettings):
    """
    Permite guardar y recuperar las diversas opciones de configuración. Expone además
    todos los atributos relacionados con las preferencias generales del usuario, que pueden
    ser leídos desde cualquier parte de la aplicación. Los atributos de la clase son:

        --  Un atributo por cada opción de cada converter. El nombre del atributo resulta
            de concatenar el tipo de archivo sobre el que opera el converter, más el nombre
            de la opción capitalizando la primer letra. Ejemplo: la opción "ignoreEmptyParagraphs"
            del docx converter, se traduce en: "docxIgnoreEmptyParagraphs". Con ese nombre es como
            la opción se guarda en disco, y como el consumer debe leer el atributo de la clase.

        --  Un atributo por cada opción de la clase Ebook. La diferencia en el nombre del atributo
            con el procedimiento descrito arriba radica en que el prefijo de cada atributo
            es: "epubOutput".

        --  Todas las keys del diccionario _SETTINGS.
    """

    _SETTINGS_GROUP = "userPreferences"

    # Lista de atributos que SettingsStore expone.
    # Key = nombre de atributo.
    # Value = valor por defecto.
    _SETTINGS = dict(editor="",
                     sigilPath="",
                     allowImageProcessing=True)

    # Agrego todas las opciones posibles de todos los converters.
    _SETTINGS.update({c.FILE_TYPE + o.name[0].upper() + o.name[1:]: o.value for c in ConverterFactory.getAllConverters() for o in c.OPTIONS})

    # Agrego todas las opciones posibles de la clase Ebook.
    _SETTINGS.update({"epubOutput" + o.name[0].upper() + o.name[1:]: o.value for o in Ebook.OPTIONS})

    def getAllSettingsForConverter(self, fileType):
        """
        Retorna todas las opciones de un converter dado. Es más que nada un
        método que facilita el poder pasarle a un converter todas las opciones guardadas, sin
        necesidad de que el consumer tenga que realizar esto:

        op1 = settings.op1
        op2 = settings.op2
        ...

        @param fileType: un string, que indica de qué converter retornar las opciones.
                         Ejemplo: "docx", "fb2".

        @return: un diccionario.
                 Key: el nombre la opción.
                 Value: el valor almacenado de la opción.
        """
        return self._getAllSettingsByPrefix(fileType)

    def getAllSettingsForEbook(self):
        """
        Similar al método getAllSettingsForConverter, pero para las opciones de
        la clase Ebook.
        """
        return self._getAllSettingsByPrefix("epubOutput")

    def __getattr__(self, item):
        if item not in SettingsStore._SETTINGS:
            raise AttributeError("'{0}' object has no attribute '{1}'".format(self.__class__.__name__, item))

        defaultValue = SettingsStore._SETTINGS[item]
        return self.value("{0}/{1}".format(SettingsStore._SETTINGS_GROUP, item), defaultValue, type(defaultValue))

    def __setattr__(self, key, value):
        if key in SettingsStore._SETTINGS:
            self.setValue("{0}/{1}".format(SettingsStore._SETTINGS_GROUP, key), value)
        else:
            object.__setattr__(self, key, value)

    def _getAllSettingsByPrefix(self, prefix):
        i = len(prefix)
        return {s[i].lower() + s[i + 1:]: getattr(self, s) for s in SettingsStore._SETTINGS if s.startswith(prefix)}

    def __init__(self):
        iniPath = os.path.join(QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.DataLocation), "epubcreator.ini")
        super().__init__(iniPath, QtCore.QSettings.IniFormat)