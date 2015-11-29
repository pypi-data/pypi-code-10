from rambutan3 import RArgs
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError
from rambutan3.check_args.range.RRange_ import RRange_


class RNumberRangeMatcher(RAbstractTypeMatcher):

    __ALLOWED_TYPE_TUPLE = (int, float)

    # noinspection PyMissingConstructor
    def __init__(self,
                 number_matcher: RAbstractTypeMatcher,
                 bound_op1: str,
                 value1: (int, float),
                 bound_op2: str=None,
                 value2: (int, float)=None):
        # Intentional: Do not call super(RAbstractTypeMatcher, self).__init__()
        RArgs.check_is_instance(number_matcher, RAbstractTypeMatcher, "matcher")
        self.__number_matcher = number_matcher
        self.__range = RRange_.create(bound_op1, value1, bound_op2, value2)

    # @override
    def matches(self, value: (int, float), matcher_error: RTypeMatcherError=None) -> bool:
        result = self.__number_matcher.matches(value, matcher_error)
        if result:
            result = (value in self.__range)
            if not result and matcher_error:
                matcher_error.add_failed_match(self, value)

        return result

    # @override
    def __eq__(self, other) -> bool:
        if not isinstance(other, RNumberRangeMatcher):
            return False
        x = (self.__range == other.__range)
        return x

    # @override
    def __hash__(self) -> int:
        x = hash(self.__range)
        return x

    # @override
    def __str__(self):
        x = "{} where {}".format(self.__number_matcher.__str__(), self.__range)
        return x
