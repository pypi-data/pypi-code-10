from rambutan3.check_args.dict.RDictEnum import RDictEnum
from rambutan3.check_args.dict.RRangeSizeDictMatcher import RRangeSizeDictMatcher


# noinspection PyPep8Naming
def EXACT_SIZE_BUILTIN_DICT(*, exact_size: int) -> RRangeSizeDictMatcher:
    x = RRangeSizeDictMatcher(RDictEnum.BUILTIN_DICT, min_size=exact_size, max_size=exact_size)
    return x
