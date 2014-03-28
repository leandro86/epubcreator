import sys
import traceback

from PyQt4 import QtGui, QtCore
import sip

from epubcreator.gui.misc import utils
from epubcreator.gui import main_window
from epubcreator import config, version


def handleUnknownException(exc_type, exc_value, exc_traceback):
    exceptionMessage = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    utils.displayExceptionErrorDialog(exceptionMessage)


if __name__ == "__main__":
    # Cualquier excepción no controlada que ocurra la redirijo a un método propio para manejarla.
    sys.excepthook = handleUnknownException

    # Necesito llamar a este método porque sino pyqt crashea cuando se cierra python (al menos en windows).
    # No crashea siempre, sino que lo hace bajo alguna circunstancias. Por ejemplo, a mi me crasheaba cuando el form
    # tenía cerca de 11 o 12 widgets.
    # http://pyqt.sourceforge.net/Docs/PyQt5/pyqt4_differences.html, dice lo siguiente:
    # When the Python interpreter exits PyQt4 (by default) calls the C++ destructor of all wrapped instances
    # that it owns. This happens in a random order and can therefore cause the interpreter to crash. This behavior
    # can be disabled by calling the sip.setdestroyonexit() function.
    # PyQt5 always calls sip.setdestroyonexit() automatically.
    sip.setdestroyonexit(False)

    QtGui.QApplication.setDesktopSettingsAware(True)

    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(config.getAppIcon())

    # Intento cargar las traducciones a español para todos los diálogos, botones, etc., estándares de Qt.
    locale = QtCore.QLocale.system().name()
    qtTranslator = QtCore.QTranslator()
    if qtTranslator.load(config.QT_SP_TRANSLATION_PATH):
        app.installTranslator(qtTranslator)

    QtCore.QCoreApplication.setApplicationName(version.APP_NAME)
    QtCore.QCoreApplication.setOrganizationName(version.ORGANIZATION)
    QtCore.QCoreApplication.setOrganizationDomain(version.ORGANIZATION_DOMAIN)
    QtCore.QCoreApplication.setApplicationVersion(version.VERSION)

    mainWindow = main_window.MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())