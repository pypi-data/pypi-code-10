from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.dict.RDictEnum import RDictEnum
from rambutan3.check_args.dict.RRangeSizeDictOfMatcher import RRangeSizeDictOfMatcher


# noinspection PyPep8Naming
def NON_EMPTY_BUILTIN_DICT_OF(*,
                              key_matcher: RAbstractTypeMatcher=None,
                              value_matcher: RAbstractTypeMatcher=None) -> RRangeSizeDictOfMatcher:
    x = RRangeSizeDictOfMatcher(RDictEnum.BUILTIN_DICT,
                                key_matcher=key_matcher,
                                value_matcher=value_matcher,
                                min_size=1)
    return x