from rambutan3.check_args.set.RRangeSizeSetMatcher import RRangeSizeSetMatcher
from rambutan3.check_args.set.RSetEnum import RSetEnum


# noinspection PyPep8Naming
def EXACT_SIZE_BUILTIN_FROZENSET(*, exact_size: int) -> RRangeSizeSetMatcher:
    x = RRangeSizeSetMatcher(RSetEnum.BUILTIN_FROZENSET, min_size=exact_size, max_size=exact_size)
    return x
