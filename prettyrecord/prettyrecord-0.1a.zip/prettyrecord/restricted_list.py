"""
Module contains RestrictedList that allows to implement ListField.
"""

from collections import MutableSequence
import types


class RestrictedList(MutableSequence):
    """
    List that holds only valid values specified by constraint function.
    """

    def __init__(self, constraint: types.FunctionType, source: list=None):
        self.constraint = constraint
        self.__data = [] if source is None else source

        if any(not self.is_valid(value) for value in self.__data):
            raise ValueError("source has elements that not satisfy constraint")

    def __len__(self):
        return len(self.__data)

    def __str__(self):
        return str(self.__data)

    def __repr__(self):
        return repr(self.__data)

    def __getitem__(self, key):
        return self.__data[key]

    def __setitem__(self, key, value):
        if self.is_valid(value):
            self.__data[key] = value
        else:
            raise ValueError(value)

    def __delitem__(self, key):
        del self.__data[key]

    def __eq__(self, other):
        return all(self[i] == other[i] for i in range(len(self)))

    def insert(self, index, value):
        if self.is_valid(value):
            self.__data.insert(index, value)
        else:
            raise ValueError(value)

    def is_valid(self, value):
        try:
            return self.constraint(value)
        except:
            return False