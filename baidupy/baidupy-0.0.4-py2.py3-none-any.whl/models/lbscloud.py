# -*- coding:utf-8 -*-
from __future__ import unicode_literals


class GeoTable(object):
    """
    位置数据表
    """
    optional_attrs = (
        'id', 'create_time', 'modify_time', '_version', 'name', 'geotype',
        'is_published'
    )

    def __init__(self, name, geotype, is_published, **kwargs):
        self.__data = {}
        self.__data['name'] = name
        self.__data['geotype'] = geotype
        self.__data['is_published'] = is_published

        for key in kwargs:
            if key not in self.optional_attrs:
                kwargs.pop(key)
        self.__data.update(kwargs)

    def __getattr__(self, attr_name):
        if attr_name in self.__data:
            return self.__data[attr_name]
        else:
            return None

    def __setattr__(self, attr_name, value):
        if attr_name == 'optional_attrs':
            pass
        if attr_name in self.optional_attrs:
            self.__data[attr_name] = value
        else:
            object.__setattr__(self, attr_name, value)

    def __unicode__(self):
        class_name = str(self.__class__).strip('<>')
        return "<{0} {1}>".format(class_name, self.name)

    def __str__(self):
        return self.__unicode__().encode('utf-8')


class Column(object):
    """
    百度 LBS 云自定义扩展列
    """
    optional_attrs = (
        'id', 'max_length', 'default_value', 'is_unique_field',
    )

    def __init__(
            self,
            name,
            key,
            type,
            is_sortfilter_field,
            is_search_field,
            is_index_field,
            **kwargs
            ):

        self.__data = {}
        self.__data['name'] = name
        self.__data['key'] = key
        self.__data['type'] = type
        self.__data['is_sortfilter_field'] = is_sortfilter_field
        self.__data['is_search_field'] = is_search_field
        self.__data['is_index_field'] = is_index_field

        _kwargs = kwargs.copy()
        for key in _kwargs:
            if key not in self.optional_attrs:
                kwargs.pop(key)
        self.__data.update(kwargs)

    def __check(self):
        return self.__data

    @property
    def data(self):
        return self.__check()

    def __unicode__(self):
        class_name = str(self.__class__).strip('<>')
        return "<{0} {1}>".format(class_name, self.data['name'])

    def __str__(self):
        return self.__unicode__().encode('utf-8')
