#-*- coding: utf-8 -*-

from bson import ObjectId as _ObjectId
from datetime import datetime


__all__ = ['ObjectId', 'String', 'Integer', 'Float', 'Long', 'List', 'Boolean', 'DateTime']


class TypeMixin(object):
    def is_valid(self, value):
        raise NotImplementedError

    def to_value(self):
        raise NotImplementedError


class ObjectId(_ObjectId, TypeMixin):
    def is_valid(self, value):
        return isinstance(value, _ObjectId)

    def to_value(self):
        return _ObjectId()


class String(str, TypeMixin):
    def is_valid(self, value):
        return isinstance(value, str)

    def to_value(self):
        return str()


class Integer(int, TypeMixin):
    def is_valid(self, value):
        return isinstance(value, int)

    def to_value(self):
        return int()


class Float(float, TypeMixin):
    def is_valid(self, value):
        return isinstance(value, float)

    def to_value(self):
        return float()


class Long(long, TypeMixin):
    def is_valid(self, value):
        return isinstance(value, long)

    def to_value(self):
        return long()


class List(list, TypeMixin):
    def is_valid(self, value):
        return isinstance(value, list)

    def to_value(self):
        return list()


class Boolean(int, TypeMixin):
    def is_valid(self, value):
        return isinstance(bool(value), bool)

    def to_value(self):
        return bool()


class DateTime(datetime, TypeMixin):
    def is_valid(self, value):
        return isinstance(value, datetime)

    def to_value(self):
        return datetime.now()
