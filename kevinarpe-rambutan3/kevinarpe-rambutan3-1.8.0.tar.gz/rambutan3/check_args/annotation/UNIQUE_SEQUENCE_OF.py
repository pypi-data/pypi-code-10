from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum
from rambutan3.check_args.seq.RUniqueSequenceOfMatcher import RUniqueSequenceOfMatcher


# noinspection PyPep8Naming
def UNIQUE_SEQUENCE_OF(matcher: RAbstractTypeMatcher) -> RUniqueSequenceOfMatcher:
    x = RUniqueSequenceOfMatcher(RSequenceEnum.SEQUENCE, matcher)
    return x
