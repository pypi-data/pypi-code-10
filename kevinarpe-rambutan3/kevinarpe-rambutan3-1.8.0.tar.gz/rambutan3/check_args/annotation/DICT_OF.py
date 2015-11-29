from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.dict.RDictEnum import RDictEnum
from rambutan3.check_args.dict.RDictOfMatcher import RDictOfMatcher


# noinspection PyPep8Naming
def DICT_OF(*,
            key_matcher: RAbstractTypeMatcher=None,
            value_matcher: RAbstractTypeMatcher=None) -> RDictOfMatcher:

    x = RDictOfMatcher(RDictEnum.DICT, key_matcher=key_matcher, value_matcher=value_matcher)
    return x
