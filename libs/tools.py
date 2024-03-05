
class NotSet:
    pass


def alias(names: list, globalsDict=globals()):
    def objectDecotraor(object):
        object.aliases = []

        for name in names:
            globalsDict[name] = object
            object.aliases.append(name)

        return object
    return objectDecotraor
