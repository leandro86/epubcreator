import re
import difflib
import pprint


def assertXhtmlsAreEqual(xml1, xml2):
    # Elimina pretty-print.
    normal1 = re.sub(r"\r?\n\s*<", "<", xml1.decode()).strip()
    normal2 = re.sub(r"\r?\n\s*<", "<", xml2.decode()).strip()

    if normal1 != normal2:
        lines1 = re.sub(r"(</\w+>)", r"\1\n", normal1).splitlines()
        lines2 = re.sub(r"(</\w+>)", r"\1\n", normal2).splitlines()

        dif = [d for d in list(difflib.Differ().compare(lines1, lines2)) if d.startswith("+") or d.startswith("-")]

        raise AssertionError("Los xhtmls no son iguales:\n\n{0}".format(pprint.pformat(dif)))