from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum
from rambutan3.check_args.seq.RUniqueSequenceOfMatcher import RUniqueSequenceOfMatcher


# noinspection PyPep8Naming
def UNIQUE_LIST_OF(type_matcher: RAbstractTypeMatcher) -> RUniqueSequenceOfMatcher:
    x = RUniqueSequenceOfMatcher(RSequenceEnum.LIST, type_matcher)
    return x
