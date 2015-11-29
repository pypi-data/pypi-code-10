from rambutan3.check_args.annotation.STR_MATCHES_REGEX import STR_MATCHES_REGEX
from rambutan3.string.RStrictIdentifier import RStrictIdentifier


STR_STRICT_IDENTIFIER = STR_MATCHES_REGEX(RStrictIdentifier.REGEX_PATTERN(), RStrictIdentifier.HUMAN_READABLE_HINT())
