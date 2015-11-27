#-*- coding: utf-8 -*-

import re
from bson import ObjectId
from .structure import Structure


__all__ = ['Document']


class Document(object):
    struct = None
    ___store = None

    class Meta:
        database = None

    class DataStore(object):
        def get(self, key):
            return self.__dict__.get(key)

        def set(self, key, value):
            self.__dict__[key] = value

        def to_dict(self):
            return self.__dict__

    def __init__(self, data=None):
        self.__store = self.DataStore()
        self.initialize(data)

    def __getattr__(self, key):
        if key in self.struct_keys:
            return self.__store.get(key)
        else:
            raise AttributeError

    def __setattr__(self, key, value):
        if key in self.struct_keys:
            self.struct.is_valid_type(key, value)
            self.__store.set(key, value)
        elif key in ['__store'] or '__store' in key:
            self.__dict__[key] = value
        else:
            raise AttributeError

    def initialize(self, data):
        if not isinstance(data, dict):
            data = dict()

        for key, value in self.struct.to_dict().items():
            result = data.get(key)
            if not result:
                result = value.to_value()
            self.__store.set(key, result)

    def pk(self):
        return self.__store.get('_id')

    @property
    def struct_keys(self):
        return list(self.struct.keys())

    @classmethod
    def colname(cls):
        return re.sub('(?!^)([A-Z]+)', r'_\1', cls.__name__).lower().__str__()

    @classmethod
    def collection(cls):
        return cls.Meta.database[cls.colname()]

    @classmethod
    def count(cls, filter=None, **kwargs):
        return cls.collection().count(filter, **kwargs)

    @classmethod
    def get(cls, key, *args, **kwargs):
        data = cls.collection().find_one({'_id': ObjectId(key)}, *args, **kwargs)
        if not data:
            return None
        return cls(data)

    @classmethod
    def get_by_cond(cls, key, value, *args, **kwargs):
        data = cls.collection().find_one({key: value}, *args, **kwargs)
        if not data:
            return None
        return cls(data)

    @classmethod
    def find(cls, *args, **kwargs):
        return [cls(x) for x in cls.collection().find(*args, **kwargs)]

    @classmethod
    def all(cls):
        return cls.find()

    @classmethod
    def exists(cls, key, value):
        if cls.collection().find_one({key: value}):
            return True
        return False

    def insert(self, generate_object_id=True):
        if generate_object_id and '_id' in self.struct_keys:
            self.__store.set('_id', ObjectId())
        return self.collection().insert_one(self.to_dict())

    @classmethod
    def insert_all(cls, documents, generate_object_id=True, ordered=True):
        results = []
        for document in documents:
            if generate_object_id:
                document._id = ObjectId()
            results += [document.to_dict()]
        return cls.collection().insert_many(results, ordered=ordered)

    def update(self, upsert=False):
        dict = self.to_dict()
        if '_id' in self.struct_keys:
            del dict['_id']
        return self.collection().update_one({'_id': self.pk()}, {'$set': dict}, upsert=upsert)

    @classmethod
    def update_all(cls, documents, update, upsert=False):
        keys = [x.pk() for x in documents]
        return cls.collection().update_many({'_id': {'$in': keys}}, update, upsert=upsert)

    def delete(self):
        if not self.pk():
            return False
        return self.collection().delete_one({'_id': self.pk()})

    @classmethod
    def delete_all(cls, filter):
        return cls.collection().delete_many(filter)

    def to_dict(self):
        return self.__store.to_dict()
