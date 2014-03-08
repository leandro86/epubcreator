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


def purgeCompiledFiles():
    """
    Elimina todos los archivos compilados que no tengan el correspondiente
    source asociado (ya sea un archivo ".ui" o ".qrc").
    """
    for file in (f for f in os.listdir(OUTPUT_DIR) if f != "__init__.py"):
        fileName = os.path.splitext(file)[0]

        if fileName.endswith("_rc"):
            srcFileExt = ".qrc"
            srcFileName = fileName[:-3] + srcFileExt
        else:
            srcFileExt = ".ui"
            srcFileName = fileName + srcFileExt

        if not os.path.exists(os.path.join(FORMS_PATH, srcFileName)):
            print(file)
            os.remove(os.path.join(OUTPUT_DIR, file))


def removeDateFromCompiledFile(file):
    """
    Elimino del archivo ".py" generado la fecha de creación, de manera tal que
    si no hubo realmente cambios en el código, entonces no sea detectado por el
    software de control de versiones.

    @param file: el nombre del archivo.
    """
    with open(file) as inputFile:
        lines = inputFile.readlines()

    with open(file, "w") as outputFile:
        lines[4] = "# Created by PyQt4 UI code generator\n"
        del (lines[5])

        outputFile.writelines(lines)


def compileUi():
    """
    Genera los archivos ".py" a partir de los ".ui" y ".qrc".
    """
    files = os.listdir(FORMS_PATH)
    for file in (f for f in files if f.endswith(".ui") or f.endswith(".qrc")):
        fileName, fileExtension = os.path.splitext(file)

        inputFile = os.path.join(FORMS_PATH, file)

        if fileExtension == ".ui":
            outputFile = os.path.join(OUTPUT_DIR, fileName + ".py")
            cmd = [PYUIC, "--from-imports", "-o", outputFile, inputFile]
        else:
            outputFile = os.path.join(OUTPUT_DIR, fileName + "_rc.py")
            cmd = [PYRCC, "-py3", "-o", outputFile, inputFile]

        subprocess.call(cmd)
        removeDateFromCompiledFile(outputFile)


if __name__ == "__main__":
    purgeCompiledFiles()
    compileUi()
    print("Listo!")