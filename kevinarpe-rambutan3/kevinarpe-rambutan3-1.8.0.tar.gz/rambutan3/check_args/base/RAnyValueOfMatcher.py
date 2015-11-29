from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError


class RAnyValueOfMatcher(RAbstractTypeMatcher):

    # noinspection PyMissingConstructor
    def __init__(self, *value_tuple):
        # Intentional: Do not call super(RAbstractTypeMatcher, self).__init__()
        if not value_tuple:
            raise ValueError("Argument '*value_tuple' is empty")
        self.__value_frozenset = frozenset(value_tuple)

    # @override
    def matches(self, value, matcher_error: RTypeMatcherError=None) -> bool:
        x = value in self.__value_frozenset

        if not x and matcher_error:
            matcher_error.add_failed_match(self, value)

        return x

    # @override
    def __eq__(self, other) -> bool:
        if not isinstance(other, RAnyValueOfMatcher):
            return False

        x = (self.__value_frozenset == other.__value_frozenset)
        return x

    # @override
    def __hash__(self) -> int:
        x = hash(self.__value_frozenset)
        return x

    # @override
    def __str__(self):
        x = "any value of {}".format(self.__value_frozenset)
        return x
