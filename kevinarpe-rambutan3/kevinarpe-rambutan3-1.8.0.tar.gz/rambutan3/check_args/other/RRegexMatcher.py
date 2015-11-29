from rambutan3 import RArgs
from rambutan3 import RTypes
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError
from rambutan3.string.RMessageText import RMessageText


class RRegexMatcher(RAbstractTypeMatcher):

    # noinspection PyMissingConstructor
    def __init__(self, regex_pattern: RTypes.REGEX_PATTERN_TYPE, human_readable_hint: RMessageText):
        # Intentional: Do not call super(RAbstractTypeMatcher, self).__init__()
        RArgs.check_is_instance(regex_pattern, RTypes.REGEX_PATTERN_TYPE, 'pattern')
        RArgs.check_is_instance(human_readable_hint, RMessageText, 'human_readable_hint')
        self.__regex_pattern = regex_pattern
        self.__human_readable_hint = human_readable_hint

    # @override
    def matches(self, value: str, matcher_error: RTypeMatcherError=None) -> bool:
        result = False
        if isinstance(value, str):
            x = self.__regex_pattern.search(value)
            result = bool(x)

        if not result and matcher_error:
            matcher_error.add_failed_match(self, value)

        return result

    # @override
    def __eq__(self, other) -> bool:
        if not isinstance(other, RRegexMatcher):
            return False

        x = (self.__regex_pattern == other.__regex_pattern)
        return x

    # @override
    def __hash__(self) -> int:
        x = hash(self.__regex_pattern)
        return x

    # @override
    def __str__(self):
        x = "str matching regex /{}/ ({})".format(self.__regex_pattern.pattern, self.__human_readable_hint)
        return x
