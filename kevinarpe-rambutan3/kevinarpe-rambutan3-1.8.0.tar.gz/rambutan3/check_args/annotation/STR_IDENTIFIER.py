from rambutan3.check_args.annotation.STR_MATCHES_REGEX import STR_MATCHES_REGEX
from rambutan3.string.RIdentifier import RIdentifier


STR_IDENTIFIER = STR_MATCHES_REGEX(RIdentifier.REGEX_PATTERN(), RIdentifier.HUMAN_READABLE_HINT())
