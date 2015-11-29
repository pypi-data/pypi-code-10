from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum
from rambutan3.check_args.seq.RSequenceOfMatcher import RSequenceOfMatcher


# noinspection PyPep8Naming
def SEQUENCE_OF(matcher: RAbstractTypeMatcher) -> RSequenceOfMatcher:
    x = RSequenceOfMatcher(RSequenceEnum.SEQUENCE, matcher)
    return x