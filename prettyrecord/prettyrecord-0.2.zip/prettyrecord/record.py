"""
Module contains Record class that allows you to create SQLAlchemy like classes.
"""

from collections import OrderedDict

from prettyrecord.name_utils import mangle_name, unmangle_name
from prettyrecord.fields import Field, RecordField

__all__ = ("Record",)


class MetaRecord(type):
    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        return OrderedDict()

    @classmethod
    def _prepare_field(mcs, field):
        if isinstance(field, Record):
            return RecordField(record_type=type(field))
        else:
            return field

    def __new__(mcs, name, bases, attrs, **kwargs):
        slots = []

        try:
            for attr_name, attr in attrs.items():
                if isinstance(attr, (Field, Record)):
                    field = attrs[attr_name] = mcs._prepare_field(attr)
                    field.name = field.name or mangle_name(name, attr_name)
                    slots.append(field.name)
        except NameError:
            pass

        for option, value in kwargs.items():
            attrs['__{}__'.format(option)] = value

        attrs['__slots__'] = tuple(slots)

        return super(MetaRecord, mcs).__new__(mcs, name, bases, attrs)

    def __init__(cls, name, bases, attrs, **kwargs):
        super(MetaRecord, cls).__init__(name, bases, attrs)

    def __setattr__(self, key, value):
        old_value = getattr(self, key)

        if (old_value is None) or (type(old_value) is type(value)):
            super(MetaRecord, self).__setattr__(key, value)
        else:
            raise AttributeError("can't modify {}'s {} attribute".format(self.__name__, key))

    def __delattr__(self, key):
        raise AttributeError("can't remove {}'s {} attribute".format(self.__name__, key))


class Record(metaclass=MetaRecord):
    """
    Record allows you to create SQLAlchemy like classes.
    You have only subclass it and fill with descriptors based on Field class.
    """

    def __init__(self, **kwargs):
        for _, field in self.iter_fields():
            field.__set__(self, field.default_value)

        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def iter_fields(cls):
        for owner in reversed(cls.__mro__):
            if issubclass(owner, Record) and owner is not Record:
                for mangled_name in owner.__slots__:
                    yield owner, getattr(owner, unmangle_name(mangled_name))

    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            return False

        return all(attr.__get__(self, None) == attr.__get__(other, None)
                    for _, attr in self.iter_fields())

    def __repr__(self):
        args = ['{}={}'.format(unmangle_name(attr.name), repr(attr.__get__(self, None)))
                for klass, attr in self.iter_fields() if klass is self.__class__]

        return '{}({})'.format(self.__class__.__name__, ', '.join(args))
