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

# Es necesario correr este script cada vez que se realice algún cambio
# en la interface gráfica.

import os
import distutils.sysconfig
import subprocess
import shutil


SITE_PACKAGES_PATH = distutils.sysconfig.get_python_lib()
PYUIC = os.path.join(SITE_PACKAGES_PATH, "PyQt4", "pyuic4.bat")
PYRCC = os.path.join(SITE_PACKAGES_PATH, "PyQt4", "pyrcc4.exe")
FORMS_PATH = os.path.join(os.path.dirname(__file__), "forms")
OUTPUT_DIR = os.path.join(FORMS_PATH, "compiled")

def compileUi():
    # Limpio primero la carpeta
    for file in [os.path.join(OUTPUT_DIR, f) for f in os.listdir(OUTPUT_DIR)]:
        if os.path.isdir(file):
            shutil.rmtree(file)
        else:
            os.remove(file)

    files = os.listdir(FORMS_PATH)
    for file in files:
        fileName, fileExtension = os.path.splitext(file)

        if fileExtension == ".ui":
            subprocess.call([PYUIC, "--from-imports", "-o", os.path.join(OUTPUT_DIR, fileName + ".py"), os.path.join(FORMS_PATH, file)])
        elif fileExtension == ".qrc":
            subprocess.call([PYRCC, "-py3", "-o", os.path.join(OUTPUT_DIR, fileName + "_rc.py"), os.path.join(FORMS_PATH, file)])


if __name__ == "__main__":
    compileUi()
    print("Listo!")