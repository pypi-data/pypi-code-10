from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.seq.RRangeSizeSequenceOfMatcher import RRangeSizeSequenceOfMatcher
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum


# noinspection PyPep8Naming
def NON_EMPTY_SEQUENCE_OF(matcher: RAbstractTypeMatcher) -> RRangeSizeSequenceOfMatcher:
    x = RRangeSizeSequenceOfMatcher(RSequenceEnum.SEQUENCE, matcher, min_size=1)
    return x
