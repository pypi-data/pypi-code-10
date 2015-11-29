from rambutan3.check_args.set.RRangeSizeSetMatcher import RRangeSizeSetMatcher
from rambutan3.check_args.set.RSetEnum import RSetEnum


# noinspection PyPep8Naming
def RANGE_SIZE_BUILTIN_FROZENSET(*, min_size: int=-1, max_size: int=-1) -> RRangeSizeSetMatcher:
    x = RRangeSizeSetMatcher(RSetEnum.BUILTIN_FROZENSET, min_size=min_size, max_size=max_size)
    return x
