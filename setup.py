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
import distutils.sysconfig

from cx_Freeze import setup, Executable

import version


_SITE_PACKAGES_PATH = distutils.sysconfig.get_python_lib()
_PYQT_PATH = os.path.join(_SITE_PACKAGES_PATH, "PyQt4")

_packages = ["lxml"]
_includes = []
#_excludes = ["PyQt4.QtNetwork"]
_include_files = [(os.path.join(_PYQT_PATH, "plugins", "imageformats", "qjpeg4.dll"), "imageformats\qjpeg4.dll"),
                  ("ecreator/files", "files"),
                  ("gui/resources/translations/qt_es.qm", "translations/qt_es.qm")]

_base = None

if sys.platform == "win32":
    _base = "Win32GUI"

setup(name = version.APP_NAME,
      version = version.VERSION,
      description = version.DESCRIPTION,
      options = {"build_exe": {"packages" : _packages,
                               "includes" : _includes,
                               "excludes" : _excludes,
                               "include_files" : _include_files,
                               "include_msvcr" : True}},
      executables = [Executable("main.py", base=_base)])