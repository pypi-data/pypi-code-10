from forbiddenfruit import curse
import itertools

class enumerable:
    @staticmethod
    def map(self, fn):
        return map(fn, self)

    @staticmethod
    def filter(self, fn):
        return filter(fn, self)

    @staticmethod
    def reduce(self, fn, initial=None):
        return reduce(fn, self, initial) if initial else reduce(fn, self)

    @staticmethod
    def take(self, number):
        return itertools.islice(self, number)

    @staticmethod
    def toList(self):
        return list(self)


curse(object, "map", enumerable.map)
curse(object, "filter", enumerable.filter)
curse(object, "reduce", enumerable.reduce)
curse(object, "take", enumerable.take)
curse(object, "toList", enumerable.toList)
