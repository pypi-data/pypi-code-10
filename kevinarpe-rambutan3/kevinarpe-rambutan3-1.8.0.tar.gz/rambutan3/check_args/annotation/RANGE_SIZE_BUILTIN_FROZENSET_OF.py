from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.set.RRangeSizeSetOfMatcher import RRangeSizeSetOfMatcher
from rambutan3.check_args.set.RSetEnum import RSetEnum


# noinspection PyPep8Naming
def RANGE_SIZE_BUILTIN_FROZENSET_OF(type_matcher: RAbstractTypeMatcher, *, min_size: int=-1, max_size: int=-1) \
        -> RRangeSizeSetOfMatcher:

    x = RRangeSizeSetOfMatcher(RSetEnum.BUILTIN_FROZENSET, type_matcher, min_size=min_size, max_size=max_size)
    return x
