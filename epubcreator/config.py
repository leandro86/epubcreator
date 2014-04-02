import os
import sys

from PyQt4 import QtCore

IS_FROZEN = getattr(sys, "frozen", False)

IS_RUNNING_ON_WIN = sys.platform == "win32"
IS_RUNNING_ON_LINUX = sys.platform == "linux"
IS_RUNNING_ON_MAC = sys.platform == "darwin"

ROOT_DIR_PATH = os.path.dirname(sys.executable if IS_FROZEN else __file__)
EPUBBASE_FILES_DIR_PATH = os.path.join(ROOT_DIR_PATH, "" if IS_FROZEN else "epubbase", "files")


def getTranslationPath():
    return os.path.join(QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath), "qt_es.qm")
