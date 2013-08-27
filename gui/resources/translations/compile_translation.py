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


SITE_PACKAGES_PATH = distutils.sysconfig.get_python_lib()
LRELEASE = os.path.join(SITE_PACKAGES_PATH, "PyQt4", "lrelease.exe")


def compileQtTranslation():
    currentDir = os.path.dirname(__file__)
    files = os.listdir(currentDir)
    fileList = ""
    
    for file in files:
        if file.endswith(".ts"):
            fileList += os.path.join(currentDir, file)

    subprocess.call([LRELEASE, fileList, "-qm", "qt_es.qm"])


if __name__ == '__main__':
    compileQtTranslation()
    print("Listo!")