from rambutan3.check_args.dict.RDictEnum import RDictEnum
from rambutan3.check_args.dict.RRangeSizeDictMatcher import RRangeSizeDictMatcher
from rambutan3.check_args.seq.RRangeSizeSequenceMatcher import RRangeSizeSequenceMatcher


# noinspection PyPep8Naming
def EXACT_SIZE_DICT(*, exact_size: int) -> RRangeSizeSequenceMatcher:
    x = RRangeSizeDictMatcher(RDictEnum.DICT, min_size=exact_size, max_size=exact_size)
    return x
