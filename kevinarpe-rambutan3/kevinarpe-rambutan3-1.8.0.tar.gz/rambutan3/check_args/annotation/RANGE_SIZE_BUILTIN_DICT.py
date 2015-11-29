from rambutan3.check_args.dict.RDictEnum import RDictEnum
from rambutan3.check_args.dict.RRangeSizeDictMatcher import RRangeSizeDictMatcher


# noinspection PyPep8Naming
def RANGE_SIZE_BUILTIN_DICT(*, min_size: int=-1, max_size: int=-1) -> RRangeSizeDictMatcher:
    x = RRangeSizeDictMatcher(RDictEnum.BUILTIN_DICT, min_size=min_size, max_size=max_size)
    return x
