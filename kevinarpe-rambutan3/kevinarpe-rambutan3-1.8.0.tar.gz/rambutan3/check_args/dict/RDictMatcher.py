from rambutan3 import RArgs
from rambutan3.check_args.base.RInstanceMatcher import RInstanceMatcher
from rambutan3.check_args.dict.RDictEnum import RDictEnum


class RDictMatcher(RInstanceMatcher):

    def __init__(self, dict_enum: RDictEnum):
        RArgs.check_is_instance(dict_enum, RDictEnum, "dict_enum")
        super().__init__(*(dict_enum.value))
