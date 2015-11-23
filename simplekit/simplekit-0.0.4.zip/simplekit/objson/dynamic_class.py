import re
from keyword import iskeyword as _iskeyword

__author__ = 'benjamin.c.yan@newegg.com'

_re_encode = re.compile('[^a-zA-z0-9_]', re.MULTILINE)


def _item_setter(key):
    def _setter(item, value):
        item[key] = value

    return _setter


def _item_getter(key):
    def _getter(item):
        return item[key]

    return _getter


def _dynamic__init(self, kv):
    self._data.update(kv)


def _dynamic__setitem(self, key, value):
    self._data[key] = value


def _property(name):
    return property(_item_getter(name), _item_setter(name))


def _encode_property_name(name):
    if _iskeyword(name) or name[0].isdigit():
        return 'm' + name
    elif not all(c.isalnum() or c == '_' for c in name):
        return _re_encode.sub('_', name)
    return name


def make_dynamic_class(typename, field_names):
    """a factory function to create type dynamically

    The factory function is used by :func:`objson.load` and :func:`objson.loads`.
    Creating the object deserialize from json string. The inspiration come from
    :func:`collections.namedtuple`. the difference is that I don't your the class
    template to define a dynamic class, instead of, I use the :func:`type` factory
    function.

    Class prototype definition:

    >>> class JsonObject(object):
    >>> __identifier__ = "dolphin"
    >>>
    >>> __slots__ = ('name', 'age')
    >>>
    >>> _data = dict()
    >>>
    >>> def __init__(self, kv):
    >>>     self._data.update(kv)
    >>>
    >>> def __getitem__(self, key):
    >>>     return self._data.get(key)
    >>>
    >>> def __setitem__(self, key, value):
    >>>     self._data[key] = value
    >>>
    >>> def __iter__(self):
    >>>     return self._data.__iter__()
    >>>
    >>> def __repr__(self):
    >>>    keys = sorted(self._data.keys())
    >>>    text = ', '.join(["%s=%r" % (key, self[key]) for key in keys])
    >>>    return '{%s}' % text
    >>>
    >>> name = property(_item_getter('name'), _item_setter('name'))
    >>> age = property(_item_getter('age'), _item_setter('age'))

    :param typename: dynamic class's name
    :param field_names: a string :class:`list` and a field name string which separated by comma,
        ``['name', 'sex']`` or ``"name,sex"``

    :return: a class type
    """
    if isinstance(field_names, basestring):
        field_names = field_names.replace(",", " ").split()
    field_names = map(str, field_names)

    safe_fields_names = map(_encode_property_name, field_names)

    attr = dict((safe_name, _property(name)) for name, safe_name in zip(field_names, safe_fields_names))
    attr['__doc__'] = typename
    attr['__identifier__'] = "dolphin"
    attr['__slots__'] = tuple(safe_fields_names)
    attr['_data'] = dict()
    attr['__init__'] = _dynamic__init
    attr['__getitem__'] = lambda self, key: self._data.get(key)
    attr['__setitem__'] = _dynamic__setitem
    attr['__iter__'] = lambda self: iter(self._data)
    attr['__repr__'] = lambda self: "{%s}" % (', '.join([
                                                            "%s=%r" % (key, self[key]) for key in
                                                            sorted(self._data.keys())
                                                            ]))

    return type(typename, (object,), attr)
