import os
import sys

from PyQt4 import QtGui

# Necesito este import para obtener el ícono de la aplicación
from gui.forms.compiled import epubcreator_rc


_isFrozen = getattr(sys, "frozen", False)

################ Algunas variables globales de interés ################
IS_RUNNING_ON_WIN = sys.platform == "win32"
IS_RUNNING_ON_LINUX = sys.platform == "linux"
IS_RUNNING_ON_MAC = sys.platform == "darwin"

############################# Directorios #############################
ROOT_DIR_PATH = os.path.dirname(sys.executable if _isFrozen else __file__)
EPUBBASE_FILES_DIR_PATH = os.path.join(ROOT_DIR_PATH, "" if _isFrozen else "epubcreator", "files", "epubbase_files")

############################# Archivos ################################
DOCX_TO_EPUB_STYLESHEET_PATH = os.path.join(ROOT_DIR_PATH, "" if _isFrozen else "epubcreator", "files", "stylesheets",
                                            "docx_to_epub.xslt")
QT_SP_TRANSLATION_PATH = os.path.join(ROOT_DIR_PATH, "" if _isFrozen else os.path.join("gui", "resources"),
                                      "translations", "qt_es.qm")


def getAppIcon():
    return QtGui.QIcon(":/epubcreator/resources/images/icons/app_icon_512x512.png")
