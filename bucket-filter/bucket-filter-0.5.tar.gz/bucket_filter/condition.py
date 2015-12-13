from enum import Enum


class ConditionType(Enum):
    BOOLEAN = 1,
    RANGE = 2,


class Condition():

    @staticmethod
    def build_key(expression):
        return expression

class BooleanCondition(Condition):
    def __init__(self, expression):
        self.expression = expression
        self.key = expression

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, key):
        self.__key = Condition.build_key(key)
