from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.set.RSetEnum import RSetEnum
from rambutan3.check_args.set.RSetOfMatcher import RSetOfMatcher


# noinspection PyPep8Naming
def BUILTIN_FROZENSET_OF(type_matcher: RAbstractTypeMatcher) -> RSetOfMatcher:
    x = RSetOfMatcher(RSetEnum.BUILTIN_FROZENSET, type_matcher)
    return x