import types
from rambutan3 import RArgs, RTypes
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.RInstanceMatcher import RInstanceMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError
from rambutan3.string.RMessageText import RMessageText


class RInstanceWithPredicateMatcher(RAbstractTypeMatcher):

    def __init__(self, predicate_func: types.FunctionType, predicate_description: RMessageText, *class_or_type_tuple):
        self.__delegate = RInstanceMatcher(*class_or_type_tuple)

        RArgs.check_is_instance(predicate_func, RTypes.FUNCTION_TYPE_TUPLE, "predicate_func")
        self.__predicate_func = predicate_func

        RArgs.check_is_instance(predicate_description, RMessageText, "predicate_description")
        self.__predicate_description = predicate_description

    # @override
    def matches(self, value, matcher_error: RTypeMatcherError=None) -> bool:
        if not self.__delegate.matches(value, matcher_error):
            return False

        try:
            x = self.__predicate_func(value)
        except Exception as e:
            if matcher_error:
                matcher_error.add_failed_match(self, value, RMessageText('Predicate [{}] threw exception: {}'
                                                                         .format(self.__predicate_description, repr(e))))
            return False

        if not isinstance(x, bool):
            if matcher_error:
                matcher_error.add_failed_match(self, value, RMessageText('Predicate [{}] did not return bool value: [{}]'
                                                                         .format(self.__predicate_description, x)))
            return False

        if not x and matcher_error:
            matcher_error.add_failed_match(self, value,
                                           RMessageText('Predicate failure: {}'.format(self.__predicate_description)))

        return x

    # @override
    def __eq__(self, other) -> bool:
        if not isinstance(other, RInstanceWithPredicateMatcher):
            return False

        # Comparing predicate functions is less than ideal here.  I don't know a better alternative.
        x = (self.__delegate == other.__delegate) \
            and (self.__predicate_func == other.__predicate_func) \
            and (self.__predicate_description == other.__predicate_description)

        return x

    # @override
    def __hash__(self) -> int:
        x = hash((self.__delegate, self.__predicate_func, self.__predicate_description))
        return x

    # @override
    def __str__(self) -> str:
        x = "{} with predicate: '{}'".format(self.__delegate, self.__predicate_description)
        return x
