from rambutan3.check_args.set.RRangeSizeSetMatcher import RRangeSizeSetMatcher
from rambutan3.check_args.set.RSetEnum import RSetEnum


NON_EMPTY_SET = RRangeSizeSetMatcher(RSetEnum.SET, min_size=1)
