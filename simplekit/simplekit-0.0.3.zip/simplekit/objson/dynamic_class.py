__author__ = 'benjamin.c.yan@newegg.com'

from keyword import iskeyword as _iskeyword


def _item_setter(key):
    def _setter(item, value):
        item[key] = value

    return _setter


def _item_getter(key):
    def _getter(item):
        return item[key]

    return _getter


def __dynamic__init__(self, kv):
    self._data.update(kv)


def __dynamic__getitem__(self, key):
    return self._data.get(key)


def __dynamic__setitem__(self, key, value):
    self._data[key] = value


def make_dynamic_class(typename, field_names):
    if isinstance(field_names, basestring):
        field_names = field_names.replace(",", " ").split()
    field_names = map(str, field_names)

    safe_fields_names = map(lambda x: 'm' + x if _iskeyword(x) else x, field_names)

    attr = dict()
    attr['__doc__'] = typename
    attr['__identifier__'] = "dolphin"
    attr['__slots__'] = tuple(safe_fields_names)
    attr['_data'] = dict()
    attr['__init__'] = __dynamic__init__
    attr['__getitem__'] = lambda self, key: self._data.get(key)
    attr['__setitem__'] = __dynamic__setitem__
    attr['__iter__'] = lambda self: iter(self._data)
    attr['__repr__'] = lambda self: "{%s}" % (', '.join([
        "%s=%r" % (key, self[key]) for key in sorted(self._data.keys())
    ]))

    for name, safe_name in zip(field_names, safe_fields_names):
        attr[safe_name] = property(_item_getter('%s' % name), _item_setter('%s' % name))

    return type(typename, (object,), attr)

