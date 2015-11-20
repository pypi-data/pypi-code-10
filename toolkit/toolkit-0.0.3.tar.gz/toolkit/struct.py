# coding=utf8

from toolkit.utils import sha1


# TODO: Write test cases.

def dict2class(data, name=None, bases=None):
    """
    Utils function to convert a dict to a class

    .. code-block:: python

        dict2class({'name': 'Demo'})
        >>> toolkit.struct.330ee1b369b814e438bd6e95cadc25a66a89b0d0
    """
    return type(name or sha1(str(data)), bases or (object,), data)


def dict2obj(data, name=None, bases=None):
    """
    Utils function to convert a dict to an object

    .. code-block:: python

        dict2obj({'name': 'Demo'})
        >>> <toolkit.struct.330ee1b369b814e438bd6e95cadc25a66a89b0d0 at 0x105440590>
    """
    dictclass = dict2class(data, name, bases)
    return dictclass()
