from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.set.RRangeSizeSetOfMatcher import RRangeSizeSetOfMatcher
from rambutan3.check_args.set.RSetEnum import RSetEnum


# noinspection PyPep8Naming
def EXACT_SIZE_BUILTIN_FROZENSET_OF(type_matcher: RAbstractTypeMatcher, *, exact_size: int) \
        -> RRangeSizeSetOfMatcher:

    x = RRangeSizeSetOfMatcher(RSetEnum.BUILTIN_FROZENSET, type_matcher, min_size=exact_size, max_size=exact_size)
    return x
