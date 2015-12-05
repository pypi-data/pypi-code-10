# coding: utf-8

def dget(dictionary, route, default=None):
    # get path
    cmd_list = route.split('.')
    tmp = dict(dictionary)

    for c in cmd_list:
        # if val is None which will cause AttributeError
        # of no method get, then return default value
        try:
            val = tmp.get(c, None)
        except AttributeError:
            # exit case 1: default
            return default

        if val!= None:
            tmp = val
        else:
            # exit case 2: default
            return default

    # exit case 3: fetched value
    return tmp

# quote from http://stackoverflow.com/questions/635483/what-is-the-best-way-to-implement-nested-dictionaries-in-python?answertab=votes#tab-top
class SetNestedDict(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

