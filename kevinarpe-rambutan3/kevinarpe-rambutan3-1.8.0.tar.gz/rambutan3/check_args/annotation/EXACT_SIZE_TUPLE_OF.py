from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.seq.RRangeSizeSequenceOfMatcher import RRangeSizeSequenceOfMatcher
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum


# noinspection PyPep8Naming
def EXACT_SIZE_TUPLE_OF(type_matcher: RAbstractTypeMatcher, *, exact_size: int) \
        -> RRangeSizeSequenceOfMatcher:

    x = RRangeSizeSequenceOfMatcher(RSequenceEnum.TUPLE, type_matcher, min_size=exact_size, max_size=exact_size)
    return x
