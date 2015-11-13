import functools


class hybrid_property(object):
    """A decorator which allows definition of a Python descriptor with both
    instance-level and class-level behavior.

    Taken from :mod:`sqlalchemy`. Do not combine.
    """

    def __init__(self, fget, fset=None, fdel=None, expr=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.expr = expr or fget
        functools.update_wrapper(self, fget)

    def __get__(self, instance, owner):
        if instance is None:
            return self.expr(owner)
        else:
            return self.fget(instance)

    def __set__(self, instance, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(instance, value)

    def __delete__(self, instance):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(instance)

    def setter(self, fset):
        """Provide a modifying decorator that defines a value-setter method."""

        self.fset = fset
        return self

    def deleter(self, fdel):
        """Provide a modifying decorator that defines a
        value-deletion method."""

        self.fdel = fdel
        return self
