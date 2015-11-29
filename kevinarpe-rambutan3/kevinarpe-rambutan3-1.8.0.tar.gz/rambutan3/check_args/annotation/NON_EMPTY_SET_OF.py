from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.set.RRangeSizeSetOfMatcher import RRangeSizeSetOfMatcher
from rambutan3.check_args.set.RSetEnum import RSetEnum


# noinspection PyPep8Naming
def NON_EMPTY_SET_OF(type_matcher: RAbstractTypeMatcher) -> RRangeSizeSetOfMatcher:
    x = RRangeSizeSetOfMatcher(RSetEnum.SET, type_matcher, min_size=1)
    return x