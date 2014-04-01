import os
import sys

################ Algunas variables globales de interés ################
IS_FROZEN = getattr(sys, "frozen", False)

IS_RUNNING_ON_WIN = sys.platform == "win32"
IS_RUNNING_ON_LINUX = sys.platform == "linux"
IS_RUNNING_ON_MAC = sys.platform == "darwin"

############################# Directorios #############################
ROOT_DIR_PATH = os.path.dirname(sys.executable if IS_FROZEN else __file__)
EPUBBASE_FILES_DIR_PATH = os.path.join(ROOT_DIR_PATH, "" if IS_FROZEN else "epubbase", "files")

############################# Archivos ################################
QT_SP_TRANSLATION_PATH = os.path.join(ROOT_DIR_PATH, "" if IS_FROZEN else os.path.join("gui", "resources"), "translations", "qt_es.qm")