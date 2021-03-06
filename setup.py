# Script para generar un ejecutable con cx_freeze en los distintos sistemas operativos.

# En windows y linux ejecutar así:
#   python3 setup.py build
# En mac:
#   python3 setup.py bdist_mac --bundle-icon=app_icon.icns

# Notas: en windows y mac se incluyen todas las dependencias necesarias para
# ejecutar la aplicación, no así en linux, donde no distribuyo las librerías de Qt, y
# por lo tanto es necesario instalarlas (cualquier versión 4.8 sirve). No distribuyo Qt
# porque puede generarse un conflicto con las librerías Qt que ya vienen instaladas de base
# en el sistema (me ha pasado con Kubuntu, por ejemplo). Además, incluso si pudiera de alguna
# manera cargar siempre las librerías Qt que yo distribuyo, ignorando las del sistema, puedo
# encontrarme con que el look de la aplicación no sea nativo (como pasa con alguna distro basada
# en KDE). La solución más simple es entonces NO distribuir Qt, y que los usuarios tengan que
# instalar esa dependencia (lo cual generalmente no es necesario porque ya viene preinstalada).

import sys
import os
import shutil
import subprocess

from PyQt4 import QtCore
from cx_Freeze import setup, Executable

from epubcreator import version, config
import epubcreator.gui


def freezeApp():
    # Necesito esta línea para que se carguen correctamente los paths de qt hacia los plugins, traducciones, etc.
    app = QtCore.QCoreApplication(sys.argv)

    options = {}

    includes = ["PyQt4", "PyQt4.QtCore", "PyQt4.QtGui"]
    packages = ["lxml"]
    excludes = ["PyQt4.QtSvg", "PyQt4.QtNetwork", "PyQt4.QtOpenGL", "PyQt4.QtScript", "PyQt4.QtSql", "PyQt4.Qsci", "PyQt4.QtXml", "PyQt4.QtTest",
                "PyQt4.uic"]
    include_files = [("epubcreator/epubbase/files", "files")]

    qtSpanishTranslation = config.getQtSpanishTranslation()

    if not os.path.exists(qtSpanishTranslation):
        raise Exception("No se encontró el archivo de traducciones.")

    include_files.append((qtSpanishTranslation, "translations/{0}".format(os.path.split(qtSpanishTranslation)[1])))

    options["icon"] = "epubcreator/gui/resources/icons/app_icon.ico"
    options["build_exe"] = "build/epubcreator"

    if config.IS_RUNNING_ON_LINUX:
        libsPath = "/usr/lib/i386-linux-gnu"
        if sys.maxsize > 2 ** 32:
            libsPath = "/usr/lib/x86_64-linux-gnu"
        include_files.append((os.path.join(libsPath, "libxml2.so.2"), "libxml2.so.2"))
        include_files.append((os.path.join(libsPath, "libxslt.so.1"), "libxslt.so.1"))
        include_files.append((os.path.join(libsPath, "libz.so"), "libz.so"))
    else:
        imageFormatsPath = os.path.join(QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.PluginsPath), "imageformats")

        if config.IS_RUNNING_ON_MAC:
            include_files.append((os.path.join(imageFormatsPath, "libqjpeg.dylib"), "plugins/imageformats/libqjpeg.dylib"))
            include_files.append(("/opt/local/lib/libjpeg.9.dylib", "libjpeg.9.dylib"))

            # Elimino el archivo ".ico": en mac el ícono es un archivo ".icns", que luego
            # me encargo de copiar manualmente.
            del (options["icon"])

            # En mac, al utilizar bdist_mac para crear el bundle, intenta leer los archivos desde el
            # directorio: "exe.macos-i386..." (algo así), independientemente de que yo especifique otro
            # directorio de destino... por eso no puedo modificarlo, y debo dejar el que crea por defecto.      
            del (options["build_exe"])

    options["packages"] = packages
    options["includes"] = includes
    options["excludes"] = excludes
    options["include_files"] = include_files
    options["include_msvcr"] = True

    if os.path.isdir("build"):
        shutil.rmtree("build", ignore_errors=True)

    setup(name=version.APP_NAME,
          version=version.VERSION,
          description=version.DESCRIPTION,
          options={"build_exe": options},
          executables=[Executable("epubcreator/gui/main.py",
                                  base="Win32GUI" if config.IS_RUNNING_ON_WIN else None,
                                  targetName="{0}{1}".format(version.APP_NAME, ".exe" if config.IS_RUNNING_ON_WIN else ""))])

    if config.IS_RUNNING_ON_WIN:
        # Necesito el archivo qt.conf vacío. Si está vacío, Qt carga todos los paths por defecto, que
        # en el caso de los plugins es el directorio "plugins".
        with open(os.path.join("build", "epubcreator", "qt.conf"), "w", encoding="utf-8"):
            pass
    elif config.IS_RUNNING_ON_MAC:
        # El bundle ".app" creado por defecto tiene el nombre de esta forma: name-version.app.
        bundlePath = "build/{0}-{1}.app".format(version.APP_NAME, version.VERSION)
        bundleMacOsDir = os.path.join(bundlePath, "Contents", "MacOS")
        bundleResourcesDir = os.path.join(bundlePath, "Contents", "Resources")

        with open(os.path.join(bundleResourcesDir, "qt.conf"), "w", encoding="utf-8") as file:
            # Deben ser comillas dobles en el path, con las simples no funciona...
            file.write('[Paths]\nPlugins = "MacOS/plugins"\n')
            file.write('[Paths]\nTranslations = "MacOS/translations"\n')

        # Necesito saber todas las librerías que se incluyen en el bundle.
        shippedFiles = os.listdir(bundleMacOsDir)

        # cx_freeze modifica los paths de las librerías que él mismo copia al bundle, pero no hace
        # lo mismo con las librerías que yo manualmente incluyo. Por eso necesito modificar sus
        # paths para que se haga referencia al bundle, y no a las librerías del sistema.
        libsToModify = [os.path.join(bundleMacOsDir, "plugins/imageformats", imgLib) for
                        imgLib in os.listdir(os.path.join(bundleMacOsDir, "plugins/imageformats"))]
        libsToModify.append(os.path.join(bundleMacOsDir, "libjpeg.9.dylib"))

        for lib in libsToModify:
            # Primero modifico el nombre de la librería.
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

        # Copio el ícono.
        shutil.copy("epubcreator/gui/resources/icons/app_icon.icns", "build/{0}-{1}.app/Contents/Resources".format(version.APP_NAME, version.VERSION))

        # Renombro el bundle, porque no quiero que el nombre incluya la versión.
        os.rename(bundlePath, "build/EpubCreator.app")
    elif config.IS_RUNNING_ON_LINUX:
        # No distribuyo Qt en linux, por lo que no necesito estos directorios.
        shutil.rmtree("build/epubcreator/imageformats", ignore_errors=True)
        shutil.rmtree("build/epubcreator/plugins", ignore_errors=True)


if __name__ == "__main__":
    epubcreator.gui.compileGui()
    freezeApp()