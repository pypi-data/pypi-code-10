from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.seq.RRangeSizeSequenceOfMatcher import RRangeSizeSequenceOfMatcher
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum


# noinspection PyPep8Naming
def RANGE_SIZE_TUPLE_OF(type_matcher: RAbstractTypeMatcher, *, min_size: int=-1, max_size: int=-1) \
        -> RRangeSizeSequenceOfMatcher:

    x = RRangeSizeSequenceOfMatcher(RSequenceEnum.TUPLE, type_matcher, min_size=min_size, max_size=max_size)
    return x
