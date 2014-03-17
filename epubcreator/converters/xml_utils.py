def getAttr(node, attr, namespaces=None):
    ns, name = attr.split(":")
    return node.get("{{{0}}}{1}".format(namespaces.get(ns), name))


def xpath(node, path, namespaces=None):
    return node.xpath(path, namespaces=namespaces)


def find(node, path, namespaces=None):
    return node.find(path, namespaces=namespaces)


def getAllText(node):
    return "".join(xpath(node, "descendant::text()"))