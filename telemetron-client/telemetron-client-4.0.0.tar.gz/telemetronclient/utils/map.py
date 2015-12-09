"""
Map module
"""


class Map(dict):
    """
    Utility class to access dictionaries keys as if they were class members.
    """

    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                self.update(arg)

        if kwargs:
            self.update(kwargs)

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]

    def update(self, d):
        for k, item in d.iteritems():
            self[k] = item
