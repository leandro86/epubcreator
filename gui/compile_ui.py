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

import os
import distutils.sysconfig
import subprocess


_SITE_PACKAGES_PATH = distutils.sysconfig.get_python_lib()
_PYUIC = os.path.join(_SITE_PACKAGES_PATH, "PyQt4", "pyuic4.bat")
_PYRCC = os.path.join(_SITE_PACKAGES_PATH, "PyQt4", "pyrcc4.exe")
_FORMS_PATH = os.path.join(os.path.dirname(__file__), "forms")

def _compileUi():
    files = os.listdir(_FORMS_PATH)
    for file in files:
        fileName, fileExtension = os.path.splitext(file)

        if fileExtension == ".ui":
            subprocess.call([_PYUIC, "--from-imports", "-o", os.path.join(_FORMS_PATH, "compiled", fileName + ".py"),
                             os.path.join(_FORMS_PATH, file)])
        elif fileExtension == ".qrc":
            subprocess.call([_PYRCC, "-py3", "-o", os.path.join(_FORMS_PATH, "compiled", fileName + "_rc.py"),
                             os.path.join(_FORMS_PATH, file)])

if __name__ == "__main__":
    _compileUi()
    print("Archivos compilados.")