

class RStr(str):
    """Basic subclass of {@link builtins#str}, but includes one very important feature:
    Instances of this class are not implicitly iterable.
    Method {@link #__iter__()} has been disabled, and throws a {@link builtins#TypeError}.

    To explicitly iterate, see {@link #iter()}.

    @see https://docs.python.org/3/library/stdtypes.html#str
    """

    # Something is weird about str ctor.  I don't think it really exists.
    # Instead, there is probably a special global built-in function also called 'str()'
    # that magically helps to construct a string.
    # def __init__(self, object='', encoding: str='utf-8', errors: str='strict'):
    #     super(str, self).__init__(object, encoding, errors)

    def __iter__(self):
        # This exception message exactly matches the standard message from iter()
        # when trying to create an iterator from a non-iterable,
        # e.g., iter(123) -> 'int' object is not iterable
        raise TypeError("'{}' object is not iterable".format(self.__class__.__name__))

    # noinspection PyMethodMayBeStatic
    def iter(self):
        x = super().__iter__()
        return x
