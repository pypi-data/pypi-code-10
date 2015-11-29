from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum
from rambutan3.check_args.seq.RUniqueSequenceOfMatcher import RUniqueSequenceOfMatcher


# noinspection PyPep8Naming
def UNIQUE_TUPLE_OF(type_matcher: RAbstractTypeMatcher) -> RUniqueSequenceOfMatcher:
    x = RUniqueSequenceOfMatcher(RSequenceEnum.TUPLE, type_matcher)
    return x
