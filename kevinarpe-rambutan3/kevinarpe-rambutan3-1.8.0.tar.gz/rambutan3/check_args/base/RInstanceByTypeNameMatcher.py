from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError
from rambutan3.string.RStrictIdentifier import RStrictIdentifier


class RInstanceByTypeNameMatcher(RAbstractTypeMatcher):

    # noinspection PyMissingConstructor
    def __init__(self, type_name: str):
        """
        @param type_name
               name of type or class, e.g., 'MyClass'

        @throws ValueError
                if {@code type_name} is not a valid {@link RIdentifier}
        @throws TypeError
                if {@code type_name} is not of type {@link str}
        """
        # Intentional: Do not call super(RAbstractTypeMatcher, self).__init__()
        self.__type_name = RStrictIdentifier(type_name)

    # @override
    def matches(self, value, matcher_error: RTypeMatcherError=None) -> bool:
        x = self.__type_name == type(value).__name__

        if not x and matcher_error:
            matcher_error.add_failed_match(self, value)

        return x

    # @override
    def __eq__(self, other) -> bool:
        if not isinstance(other, RInstanceByTypeNameMatcher):
            return False

        x = (self.__type_name == other.__type_name)
        return x

    # @override
    def __hash__(self) -> int:
        x = hash(self.__type_name)
        return x

    # @override
    def __str__(self) -> str:
        x = str(self.__type_name)
        return x
