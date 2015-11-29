from rambutan3 import RArgs
from rambutan3.check_args.base.RAbstractForwardingTypeMatcher import RAbstractForwardingTypeMatcher
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.RInstanceMatcher import RInstanceMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError


class RRestrictedInstanceMatcher(RAbstractForwardingTypeMatcher):
    """Restricted type instance matcher -- certain subclasses may be excluded.
    This class primarily exists to:
    1) restrict bools from matching ints, as bool is a subclass of int
    2) restrict strs from matching Sequence, as str is a subclass of Sequence

    This class is fully tested.

    @author Kevin Connor ARPE (kevinarpe@gmail.com)

    @see builtins#type()
    """

    # noinspection PyMissingConstructor
    def __init__(self, *,
                 allowed_class_or_type_non_empty_tuple,
                 not_allowed_class_or_type_iterable):
        """
        @param allowed_class_or_type_non_empty_tuple
               non-empty sequence of allowed value type classes, e.g., {@link int}
        @param not_allowed_class_or_type_iterable
               sequence of not allowed value type classes, e.g., {@link bool}
               may be empty

        @throws ValueError
                if {@code allowed_class_or_type_non_empty_tuple} is empty
        @throws TypeError
                if {@code allowed_class_or_type_non_empty_tuple} contains a item that is not a type/class
        """
        # Intentional: Do not call super(RAbstractForwardingTypeMatcher, self).__init__()
        RArgs.check_is_iterable(allowed_class_or_type_non_empty_tuple, "allowed_class_or_type_non_empty_tuple")
        RArgs.check_is_iterable(not_allowed_class_or_type_iterable, "not_allowed_class_or_type_iterable")
        self.__matcher = RInstanceMatcher(*allowed_class_or_type_non_empty_tuple)
        self.__not_allowed_class_or_type_tuple = tuple(not_allowed_class_or_type_iterable)

    # @overrides
    @property
    def _delegate(self) -> RAbstractTypeMatcher:
        return self.__matcher

    # @overrides
    def matches(self, value, matcher_error: RTypeMatcherError=None) -> bool:
        if not self.__matcher.matches(value, matcher_error):
            return False

        x = not isinstance(value, self.__not_allowed_class_or_type_tuple)

        if not x and matcher_error:
            matcher_error.add_failed_match(self, value)

        return x
