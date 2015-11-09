import distutils
from .collections.checks import is_collection, is_empty

def booleanize(truthy, blank_value=False):
    if truthy is None:
        return blank_value
    elif isinstance(truthy, basestring):
        if truthy:
            try:
                return bool(distutils.util.strtobool(truthy))
            except ValueError:
                return True
        else:
            return blank_value
    elif is_collection(truthy):
        return not is_empty(truthy)
    else:
        return bool(truthy)
