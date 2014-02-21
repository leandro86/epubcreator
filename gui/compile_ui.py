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
            if not (file.endswith("__init__.py")):
                os.remove(file)

    files = os.listdir(FORMS_PATH)
    for file in files:
        fileName, fileExtension = os.path.splitext(file)

        if fileExtension == ".ui":
            subprocess.call([PYUIC, "--from-imports", "-o", os.path.join(OUTPUT_DIR, fileName + ".py"),
                             os.path.join(FORMS_PATH, file)])
        elif fileExtension == ".qrc":
            subprocess.call(
                [PYRCC, "-py3", "-o", os.path.join(OUTPUT_DIR, fileName + "_rc.py"), os.path.join(FORMS_PATH, file)])


if __name__ == "__main__":
    compileUi()
    print("Listo!")