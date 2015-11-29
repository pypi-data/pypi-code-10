from rambutan3.check_args.dict.RDictEnum import RDictEnum
from rambutan3.check_args.dict.RRangeSizeDictMatcher import RRangeSizeDictMatcher
from rambutan3.check_args.seq.RRangeSizeSequenceMatcher import RRangeSizeSequenceMatcher


# noinspection PyPep8Naming
def RANGE_SIZE_DICT(*, min_size: int=-1, max_size: int=-1) -> RRangeSizeSequenceMatcher:
    x = RRangeSizeDictMatcher(RDictEnum.DICT, min_size=min_size, max_size=max_size)
    return x
