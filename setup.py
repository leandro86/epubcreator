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
import shutil

from PyQt4 import QtCore
from cx_Freeze import setup, Executable

import version

# En windows y linux ejecutar así: python3 setup.py build
# En Mac: python3 setup.py bdist_mac --bundle-icon=app_icon.icns

def getImageFormatsPath():
    app = QtCore.QCoreApplication(sys.argv)
    libraryPaths = QtCore.QCoreApplication.libraryPaths()

    imageFormatsPath = ""
    i = 0
    while i < len(libraryPaths) and not imageFormatsPath:
        if "plugins" in libraryPaths[i]:
            imageFormatsPath = os.path.join(libraryPaths[i], "imageformats")
        i += 1

    if imageFormatsPath:
        return imageFormatsPath
    else:
        raise "Missing qt imageformats directory!"


def freezeApp():
    imageFormatsPath = getImageFormatsPath()

    packages = ["lxml"]
    excludes = ["PyQt4.QtSvg", "PyQt4.QtNetwork", "PyQt4.QtOpenGL", "PyQt4.QtScript", "PyQt4.QtSql", "PyQt4.Qsci", "PyQt4.QtXml", "PyQt4.QtTest"]
    include_files = [(imageFormatsPath, "imageformats" if sys.platform != "darwin" else "plugins/imageformats"),
                     ("ecreator/files", "files"),
                     ("gui/resources/translations/qt_es.qm", "translations/qt_es.qm")]

    executableName = "{0}.exe".format(version.APP_NAME)
    base = "Win32GUI"

    options = {"packages": packages,
               "excludes": excludes,
               "include_files": include_files,
               "include_msvcr": True}

    if sys.platform != "win32":
        base = None
        executableName = version.APP_NAME

    if sys.platform != "darwin":
        # Ícono para windows y linux... En mac el ícono debe tener extensión icns.
        options["icon"] = "gui/resources/images/icons/app_icon.ico"

        # En mac, al utilizar bdist_mac para crear el bundle, intenta leer los archivos desde el
        # directorio: "exe.macos-i386..." (algo así), independientemente de que yo especifique otro
        # directorio de destino... por eso no puedo decirle que el directorio de destino sea "build/epubcreator", solamente
        # puedo hacerlo si estoy en windows o linux.
        options["build_exe"] = "build/epubcreator"

    setup(name=version.APP_NAME,
          version=version.VERSION,
          description=version.DESCRIPTION,
          options={"build_exe": options},
          executables=[Executable("main.py", base=base, targetName=executableName)])

    if sys.platform == "darwin":
        shutil.copyfile("gui/resources/images/icons/app_icon.icns", "{0}-{1}/Contents/Resources".format(version.APP_NAME, version.VERSION))


if __name__ == "__main__":
    freezeApp()

