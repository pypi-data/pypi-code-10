from rambutan3 import RTypes
from rambutan3.check_args.other.RRegexMatcher import RRegexMatcher
from rambutan3.string.RMessageText import RMessageText


# noinspection PyPep8Naming
def STR_MATCHES_REGEX(regex_pattern: RTypes.REGEX_PATTERN_TYPE, human_readable_hint: str) -> RRegexMatcher:
    human_readable_hint2 = RMessageText(human_readable_hint)
    x = RRegexMatcher(regex_pattern, human_readable_hint2)
    return x
