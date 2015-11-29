from rambutan3.check_args.dict.RDictEnum import RDictEnum
from rambutan3.check_args.dict.RRangeSizeDictMatcher import RRangeSizeDictMatcher


NON_EMPTY_DICT = RRangeSizeDictMatcher(RDictEnum.DICT, min_size=1)
