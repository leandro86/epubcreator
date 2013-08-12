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

from PyQt4 import QtCore
from cx_Freeze import setup, Executable

import version


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
    excludes = ["PyQt4.QtSvg", "PyQt4.QtNetwork", "PyQt4.QtOpenGL", "PyQt4.QtScript", "PyQt4.QtSql", "PyQt4.Qsci",
                "PyQt4.QtXml", "PyQt4.QtTest"]
    include_files = [(imageFormatsPath, "imageformats"),
                     ("ecreator/files", "files"),
                     ("gui/resources/translations/qt_es.qm", "translations/qt_es.qm")]
    icon = "gui/resources/images/icons/app_icon.ico"

    executableName = "epubcreator.exe"
    base = "Win32GUI"

    if sys.platform != "win32":
        base = None
        executableName = "epubcreator"

    setup(name=version.APP_NAME,
          version=version.VERSION,
          description=version.DESCRIPTION,
          options={"build_exe": {"build_exe": "build/epubcreator",
                                 "packages": packages,
                                 "excludes": excludes,
                                 "include_files": include_files,
                                 "include_msvcr": True,
                                 "icon": icon}},
          executables=[Executable("main.py",
                                  base=base,
                                  targetName=executableName)])


if __name__ == "__main__":
    freezeApp()

