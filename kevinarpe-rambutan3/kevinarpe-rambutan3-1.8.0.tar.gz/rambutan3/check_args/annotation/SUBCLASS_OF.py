from functools import lru_cache
from rambutan3.check_args.base.RSubclassMatcher import RSubclassMatcher


# noinspection PyPep8Naming
@lru_cache(maxsize=None)
def SUBCLASS_OF(class_or_type: type) -> RSubclassMatcher:
    x = RSubclassMatcher(class_or_type)
    return x