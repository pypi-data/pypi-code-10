from rambutan3.check_args.RCheckArgs import check_args
from rambutan3.check_args.annotation.ITERABLE_OF import ITERABLE_OF
from rambutan3.check_args.annotation.TYPE_MATCHER import TYPE_MATCHER


# Combine with RIterableUtil.make_iterable() to make new friends...
# See ROpSysUtil.access() for a working example.

# noinspection PyPep8Naming
@check_args
def ZERO_OR_MORE_OF(matcher: TYPE_MATCHER) -> TYPE_MATCHER:
    x = matcher | ITERABLE_OF(matcher)
    return x
