import re

from rambutan3.check_args.annotation.STR_MATCHES_REGEX import STR_MATCHES_REGEX


# At least one non-whitespace character
__REGEX = re.compile(r"^\s*\S+")


# TODO: Test me
STR_MESSAGE_TEXT = STR_MATCHES_REGEX(__REGEX, "human-readable message")
