from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.seq.RRangeSizeUniqueSequenceOfMatcher import RRangeSizeUniqueSequenceOfMatcher
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum


# noinspection PyPep8Naming
def NON_EMPTY_UNIQUE_TUPLE_OF(type_matcher: RAbstractTypeMatcher) \
        -> RRangeSizeUniqueSequenceOfMatcher:

    x = RRangeSizeUniqueSequenceOfMatcher(RSequenceEnum.TUPLE, type_matcher, min_size=1)
    return x
