from functools import lru_cache

from rambutan3.check_args.base.RStrictInstanceMatcher import RStrictInstanceMatcher


# noinspection PyPep8Naming
@lru_cache(maxsize=None)
def STRICT_INSTANCE_OF(class_or_type: type) -> RStrictInstanceMatcher:
    x = RStrictInstanceMatcher(class_or_type)
    return x
