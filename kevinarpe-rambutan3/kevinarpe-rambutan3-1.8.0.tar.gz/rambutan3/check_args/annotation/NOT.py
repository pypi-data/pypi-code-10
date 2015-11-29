from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.RLogicalNotTypeMatcher import RLogicalNotTypeMatcher


# noinspection PyPep8Naming
def NOT(matcher: RAbstractTypeMatcher):
    x = RLogicalNotTypeMatcher(matcher)
    return x
