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

# Script para generar un ejecutable con cx_freeze en los distintos sistemas operativos.
# En windows y linux ejecutar así: python3 setup.py build
# En mac: python3 setup.py bdist_mac --bundle-icon=app_icon.icns
# Notas: en windows y mac se incluyen todas las dependencias necesarias para
# ejecutar la aplicación, no así en linux, donde no distribuyo las librerías de Qt, y
# por lo tanto es necesario instalarlas (al menos la versión 4.8).
# TODO: corregir el problema con Qt y KDE para evitar tener que preinstalar las librerías Qt en linux.

import sys
import os
import shutil
import subprocess

from PyQt4 import QtCore
from cx_Freeze import setup, Executable

import version
import config


def getImgFormatsPluginsPath():
    app = QtCore.QCoreApplication(sys.argv)
    libraryPaths = QtCore.QCoreApplication.libraryPaths()

    imgFormatsPath = ""
    i = 0
    while i < len(libraryPaths) and not imgFormatsPath:
        if "plugins" in libraryPaths[i]:
            imgFormatsPath = os.path.join(libraryPaths[i], "imageformats")
        i += 1

    if imgFormatsPath:
        return imgFormatsPath
    else:
        raise "Missing qt imageformats directory!"

        
def freezeApp():
    options = {}
    
    includes = ["PyQt4", "PyQt4.QtCore", "PyQt4.QtGui"]
    packages = ["lxml"]
    excludes = ["PyQt4.QtSvg", "PyQt4.QtNetwork", "PyQt4.QtOpenGL", "PyQt4.QtScript", "PyQt4.QtSql", "PyQt4.Qsci", "PyQt4.QtXml", "PyQt4.QtTest"]
    include_files = [("ecreator/files", "files"),
                     ("gui/resources/translations/qt_es.qm", "translations/qt_es.qm")]

    options["icon"] = "gui/resources/images/icons/app_icon.ico"    
    options["build_exe"] = "build/epubcreator"          

    if config.IS_RUNNING_ON_LINUX:
        libsPath = "/usr/lib/i386-gnu-linux"
        if sys.maxsize > 2**32:
            libsPath = "/usr/lib/x86_64-linux-gnu"
        include_files.append((os.path.join(libsPath, "libxslt.so.1"), "libxslt.so.1"))
        include_files.append((os.path.join(libsPath, "libexslt.so.0"), "libexslt.so.0"))
        include_files.append((os.path.join(libsPath, "libxml2.so.2"), "libxml2.so.2"))
        include_files.append((os.path.join(libsPath, "libz.so"), "libz.so"))
    else:
        imgPluginsPath = getImgFormatsPluginsPath()

        if config.IS_RUNNING_ON_WIN:
            include_files.append((os.path.join(imgPluginsPath, "qjpeg4.dll"), "plugins/imageformats/qjpeg4.dll"))
        elif config.IS_RUNNING_ON_MAC:
            include_files.append((os.path.join(imgPluginsPath, "libqjpeg.dylib"), "plugins/imageformats/libqjpeg.dylib"))
            include_files.append(("/opt/local/lib/libjpeg.9.dylib", "libjpeg.9.dylib"))

            # Elimino el archivo ".ico": en mac el ícono es un archivo ".icns", que luego
            # me encargo de copiar manualmente
            del(options["icon"])
            
            # En mac, al utilizar bdist_mac para crear el bundle, intenta leer los archivos desde el
            # directorio: "exe.macos-i386..." (algo así), independientemente de que yo especifique otro
            # directorio de destino... por eso no puedo modificarlo, y debo dejar el que crea por defecto.      
            del(options["build_exe"])

    options["packages"] = packages
    options["includes"] = includes
    options["excludes"] = excludes
    options["include_files"] = include_files
    options["include_msvcr"] = True

    if os.path.isdir("build"):
        shutil.rmtree("build")

    setup(name=version.APP_NAME,
          version=version.VERSION,
          description=version.DESCRIPTION,
          options={"build_exe": options},
          executables=[Executable("main.py",
                                  base="Win32GUI" if config.IS_RUNNING_ON_WIN else None,
                                  targetName="{0}{1}".format(version.APP_NAME, ".exe" if config.IS_RUNNING_ON_WIN else ""))])

    if config.IS_RUNNING_ON_WIN:
        # Necesito el archivo qt.conf vacío. Si está vacío, Qt carga todos los paths por defecto, que
        # en el caso de los plugins es el directorio "plugins".
        with open(os.path.join("build", "epubcreator", "qt.conf"), "w", encoding="utf-8") as file:
            pass

    if config.IS_RUNNING_ON_MAC:
        # El bundle ".app" creado, por defecto tiene el nombre de esta forma: name-version.app
        bundlePath = "build/{0}-{1}.app".format(version.APP_NAME, version.VERSION)
        bundleMacOsDir = os.path.join(bundlePath, "Contents", "MacOS")
        bundleResourcesDir = os.path.join(bundlePath, "Contents", "Resources")

        with open(os.path.join(bundleResourcesDir, "qt.conf"), "w", encoding="utf-8") as file:
            # Deben ser comillas dobles en el path, con las simples no funciona...
            file.write('[Paths]\nPlugins = "MacOS/plugins"\n')

        # Necesito saber todas las librerías que se incluyen en el bundle
        shippedFiles = os.listdir(bundleMacOsDir)

        # cx_freeze modifica los paths de las librerías que él mismo copia al bundle, pero no hace
        # lo mismo con las librerías que yo manualmente incluyo. Por eso necesito modificar sus
        # paths para que se haga referencia al bundle, y no a las librerías del sistema
        libsToModify = [os.path.join(bundleMacOsDir, "plugins/imageformats", imgLib) for
                        imgLib in os.listdir(os.path.join(bundleMacOsDir, "plugins/imageformats"))]
        libsToModify.append(os.path.join(bundleMacOsDir, "libjpeg.9.dylib"))

        for lib in libsToModify:
            # Primero modifico el nombre de la librería
            subprocess.call(("install_name_tool", "-id", "@executable_path/{0}".format(os.path.basename(lib)), lib))

            # Acá leo cuáles son las otras librerías referencias por la librería actual que estoy procesando.
            # El comando "otool" en mac es similar al "ldd" de linux.
            otool = subprocess.Popen(("otool", "-L", lib), stdout=subprocess.PIPE)
            referencedLibs = otool.stdout.readlines()

            for referencedLib in referencedLibs:
                # Ahora, por cada librería referenciada, necesito saber si es una de las
                # librerías que se incluyen en el bundle, y en dicho caso modificar el path
                # para que apunte al path del ejecutable.
                referencedLib = referencedLib.decode()
                filename, _, _ = referencedLib.strip().partition(" ")
                prefix, name = os.path.split(filename)
                if name in shippedFiles:
                    newfilename = "@executable_path/{0}".format(name)
                    subprocess.call(("install_name_tool", "-change", filename, newfilename, lib))

        # Por último, copio el ícono
        shutil.copy("gui/resources/images/icons/app_icon.icns", "build/{0}-{1}.app/Contents/Resources".format(version.APP_NAME, version.VERSION))


if __name__ == "__main__":
    freezeApp()

