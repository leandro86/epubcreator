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

import sys
import os

from PyQt4 import QtGui, QtCore
import sip

from gui import main_window
import config, version


if __name__ == "__main__":
    # Necesito llamar a este método porque sino pyqt crashea cuando se cierra python (al menos en windows).
    # No crashea siempre, sino que lo hace bajo alguna circunstancias. Por ejemplo, a mi me crasheaba cuando el form
    # tenía cerca de 11 o 12 widgets.
    # http://pyqt.sourceforge.net/Docs/PyQt5/pyqt4_differences.html, dice lo siguiente:
    # When the Python interpreter exits PyQt4 (by default) calls the C++ destructor of all wrapped instances
    # that it owns. This happens in a random order and can therefore cause the interpreter to crash. This behavior
    # can be disabled by calling the sip.setdestroyonexit() function.
    # PyQt5 always calls sip.setdestroyonexit() automatically.
    sip.setdestroyonexit(False)

    app = QtGui.QApplication(sys.argv)

    # Intento cargar las traducciones a español para todos los diálogos, botones, etc., estándares de Qt
    locale = QtCore.QLocale.system().name()
    qtTranslator = QtCore.QTranslator()
    if qtTranslator.load(os.path.join(config.TRANSLATIONS_DIR_PATH, "qt_es")):
        app.installTranslator(qtTranslator)

    QtCore.QCoreApplication.setApplicationName(version.APP_NAME)
    QtCore.QCoreApplication.setOrganizationName(version.ORGANIZATION)
    QtCore.QCoreApplication.setOrganizationDomain(version.ORGANIZATION_DOMAIN)
    QtCore.QCoreApplication.setApplicationVersion(version.VERSION)

    mainWindow = main_window.MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())