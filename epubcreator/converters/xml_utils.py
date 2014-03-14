# def isTag(node, tag, namespaces=None):
#     ns, name = tag.split(":")
#     return "{{{0}}}{1}".format(namespaces.get(ns), name) == node.tag
#
#
# def getBarename(node):
#     tag = node.tag.split("}")[1]
#     return "{0}:{1}".format(node.prefix, tag)


def getAttr(node, attr, namespaces=None):
    ns, name = attr.split(":")
    return node.get("{{{0}}}{1}".format(namespaces.get(ns), name))


def xpath(node, path, namespaces=None):
    return node.xpath(path, namespaces=namespaces)


def find(node, path, namespaces=None):
    return node.find(path, namespaces=namespaces)


def getAllText(node):
    return "".join(xpath(node, "descendant::text()"))


# def hasText(node):
    # if node.text and node.text.strip():
    #     return True
    # else:
    #     for child in node:
    #         if (child.tail and child.tail.strip()) or hasText(child):
    #             return True
    #     return False
