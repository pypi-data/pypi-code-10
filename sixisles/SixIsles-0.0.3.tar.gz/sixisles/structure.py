#-*- coding: utf-8 -*-

__all__ = ['Structure']


class Structure(dict):
    def __init__(self, *args, **kwargs):
        super(Structure, self).__init__(*args, **kwargs)
        self.__dict__ = self
        self._validate()

    def _validate(self):
        pass

    def to_dict(self):
        return self.__dict__

    def is_valid_type(self, key, value):
        struct_type = self.__dict__.get(key)
        if not struct_type.is_valid(value):
            raise Exception

    def get_type(self, key):
        return self.to_dict().get(key)
