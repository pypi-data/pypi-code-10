from rambutan3.check_args.set.RRangeSizeSetMatcher import RRangeSizeSetMatcher
from rambutan3.check_args.set.RSetEnum import RSetEnum


NON_EMPTY_BUILTIN_FROZENSET = RRangeSizeSetMatcher(RSetEnum.BUILTIN_FROZENSET, min_size=1)
