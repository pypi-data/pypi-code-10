from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.seq.RRangeSizeUniqueSequenceOfMatcher import RRangeSizeUniqueSequenceOfMatcher
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum


# noinspection PyPep8Naming
def RANGE_SIZE_UNIQUE_SEQUENCE_OF(matcher: RAbstractTypeMatcher, *, min_size: int=-1, max_size: int=-1) \
        -> RRangeSizeUniqueSequenceOfMatcher:

    x = RRangeSizeUniqueSequenceOfMatcher(RSequenceEnum.SEQUENCE, matcher, min_size=min_size, max_size=max_size)
    return x
