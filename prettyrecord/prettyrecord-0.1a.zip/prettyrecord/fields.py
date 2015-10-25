"""
Module contains base classes for user's custom fields.
"""

__all__ = ("Field", "ListField", "RecordField")


class Field:
    def __init__(self, name='', default_value=None, required=False):
        self.name = name
        self.required = required
        self.default_value = default_value

    def __get__(self, instance, owner):
        return getattr(instance, self._name, self._default_value) if instance is not None else self

    def __set__(self, instance, value):
        setattr(instance, self._name, self.normalize(value))

    def __delete__(self, instance):
        delattr(instance, self._name)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str):
            self._name = value
        else:
            raise TypeError('should be string')

    @property
    def default_value(self):
        return self._default_value

    @default_value.setter
    def default_value(self, value):
        self._default_value = self.normalize(value)

    @property
    def required(self):
        return self._required

    @required.setter
    def required(self, value):
        if isinstance(value, bool):
            self._required = value
        else:
            raise TypeError('should be bool')

    def is_valid(self, value):
        try:
            self.normalize(value)
            return True
        except:
            return False

    def normalize(self, value):
        if self._required and value is None:
            raise ValueError("None is not allowed")

        return value


import inspect

from prettyrecord.restricted_list import RestrictedList


class ListField(Field):
    def __init__(self, element_constraint=lambda value: True, **kwargs):
        self.constraint = element_constraint

        super(ListField, self).__init__(default_value=[], **kwargs)

    def normalize(self, value):
        if value is None:
            return super(ListField, self).normalize(value)
        else:
            return RestrictedList(self.constraint, value)

    @property
    def constraint(self):
        return self._constraint

    @constraint.setter
    def constraint(self, value):
        parameters_count = len(inspect.signature(value).parameters)

        if parameters_count == 1:
            self._constraint = value
        else:
            raise ValueError('constraint should have one parameter only')


class RecordField(Field):
    def __init__(self, record_type, **kwargs):
        self.record_type = record_type

        super(RecordField, self).__init__(**kwargs)

    def normalize(self, value):
        if not isinstance(value, self._record_type) and value is not None:
            raise TypeError('should be instance of {}'.format(self._record_type.__qualname__))

        return super(RecordField, self).normalize(value)

    @property
    def record_type(self):
        return self._record_type

    @record_type.setter
    def record_type(self, value):
        if issubclass(value, Record):
            self._record_type = value
        else:
            raise TypeError('should be subclass of Record')


from prettyrecord.record import Record