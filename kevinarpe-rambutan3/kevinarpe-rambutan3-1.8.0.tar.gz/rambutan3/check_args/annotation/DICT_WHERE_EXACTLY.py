from rambutan3.check_args.dict.RDictEnum import RDictEnum
from rambutan3.check_args.dict.RDictWhereMatcher import RDictWhereMatcher


# noinspection PyPep8Naming
def DICT_WHERE_EXACTLY(matcher_dict: dict) -> RDictWhereMatcher:
    x = RDictWhereMatcher(RDictEnum.DICT, matcher_dict, is_exact=True)
    return x
