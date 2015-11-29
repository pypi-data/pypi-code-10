from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.seq.RRangeSizeSequenceOfMatcher import RRangeSizeSequenceOfMatcher
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum


# noinspection PyPep8Naming
def EXACT_SIZE_SEQUENCE_OF(matcher: RAbstractTypeMatcher, *, exact_size: int) \
        -> RRangeSizeSequenceOfMatcher:

    x = RRangeSizeSequenceOfMatcher(RSequenceEnum.SEQUENCE, matcher, min_size=exact_size, max_size=exact_size)
    return x
