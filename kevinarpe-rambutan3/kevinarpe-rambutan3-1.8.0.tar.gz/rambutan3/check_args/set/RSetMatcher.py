from rambutan3 import RArgs
from rambutan3.check_args.base.RInstanceMatcher import RInstanceMatcher
from rambutan3.check_args.set.RSetEnum import RSetEnum


class RSetMatcher(RInstanceMatcher):

    def __init__(self, set_enum: RSetEnum):
        RArgs.check_is_instance(set_enum, RSetEnum, "set_enum")
        super().__init__(*(set_enum.value))
