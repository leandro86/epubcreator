import os

from epubcreator import config

_FORMS_DIR = os.path.join(os.path.dirname(__file__), "forms")
_IMAGES_DIR = os.path.join(os.path.dirname(__file__), "resources", "images")


def compileGui():
    _compileResources()
    _compileForms()


def _getPathToPyrcc():
    import distutils.sysconfig

    pyqtInstallPath = os.path.join(distutils.sysconfig.get_python_lib(), "PyQt4")
    return next(os.path.join(pyqtInstallPath, f) for f in os.listdir(pyqtInstallPath) if f.startswith("pyrcc4"))


def _findForms():
    return [os.path.join(_FORMS_DIR, f) for f in os.listdir(_FORMS_DIR) if f.endswith(".ui")]


def _findResources():
    return [os.path.join(_IMAGES_DIR, f) for f in os.listdir(_IMAGES_DIR) if f.endswith(".qrc")]


def _compileForms():
    from PyQt4.uic import compileUi

    forms = _findForms()

    for form in forms:
        formName = os.path.split(form)[1]
        compiledFormName = "{0}_ui.py".format(os.path.splitext(formName)[0])
        pathToCompiledForm = os.path.join(_FORMS_DIR, compiledFormName)

        if not os.path.exists(pathToCompiledForm) or os.stat(form).st_mtime > os.stat(pathToCompiledForm).st_mtime:
            with open(pathToCompiledForm, "w", encoding="utf-8") as file:
                compileUi(form, file, from_imports=True)


def _compileResources():
    import subprocess

    pyrcc = _getPathToPyrcc()
    resources = _findResources()

    for resource in resources:
        resourceName = os.path.split(resource)[1]
        compiledResourceName = "{0}_rc.py".format(os.path.splitext(resourceName)[0])
        pathToCompiledResource = os.path.join(_FORMS_DIR, compiledResourceName)

        if not os.path.exists(pathToCompiledResource) or os.stat(resource).st_mtime > os.stat(pathToCompiledResource).st_mtime:
            subprocess.call([pyrcc, "-py3", resource, "-o", pathToCompiledResource])


if not config.IS_FROZEN:
    compileGui()