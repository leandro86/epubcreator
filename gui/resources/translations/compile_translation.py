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