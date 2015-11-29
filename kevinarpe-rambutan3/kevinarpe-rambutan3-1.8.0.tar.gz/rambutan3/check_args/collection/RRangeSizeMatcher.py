from rambutan3 import RArgs
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError
from rambutan3.string.RMessageText import RMessageText


class RRangeSizeMatcher(RAbstractTypeMatcher):
    """
    This class is fully tested.
    """

    # noinspection PyMissingConstructor
    def __init__(self, *, min_size: int=-1, max_size: int=-1):
        self.__check_sizes(min_size=min_size, max_size=max_size)
        self.__min_size = min_size
        self.__max_size = max_size

    @staticmethod
    def __check_sizes(*, min_size: int, max_size: int):
        RArgs.check_is_instance(min_size, int, 'min_size')
        RArgs.check_is_instance(max_size, int, 'max_size')
        if -1 == min_size and -1 == max_size:
            raise ValueError("Both args 'min_size' and 'max_size' are -1")
        if min_size < -1:
            raise ValueError("Arg 'min_size' must be >= -1: {}".format(min_size))
        if max_size < -1:
            raise ValueError("Arg 'max_size' must be >= -1: {}".format(max_size))
        if -1 != min_size and -1 != max_size and min_size > max_size:
            raise ValueError("Arg 'min_size' > arg 'max_size': {} > {}".format(min_size, max_size))

    # @override
    def matches(self, collection, matcher_error: RTypeMatcherError=None) -> bool:
        try:
            size = len(collection)
        except TypeError as e:
            # TypeError: object of type 'xyz' has no len()
            if matcher_error:
                matcher_error.add_failed_match(self, collection, RMessageText(str(e)))

            return False


        if (-1 == self.__min_size or size >= self.__min_size) \
        and (-1 == self.__max_size or size <= self.__max_size):
            return True

        if matcher_error:
            matcher_error.add_failed_match(self, collection, RMessageText('Actual size is {}'.format(size)))

        return False

    # @override
    def __eq__(self, other) -> bool:
        if not isinstance(other, RRangeSizeMatcher):
            return False
        x = ((self.__min_size == other.__min_size) and (self.__max_size == other.__max_size))
        return x

    # @override
    def __hash__(self) -> int:
        x = hash((self.__min_size, self.__max_size))
        return x

    # @override
    def __str__(self):
        x = ''
        if -1 != self.__min_size:
            x += 'size >= {}'.format(self.__min_size)

        if -1 != self.__max_size:
            if x:
                x += ' and '
            x += 'size <= {}'.format(self.__max_size)

        x = ' where ' + x
        return x
