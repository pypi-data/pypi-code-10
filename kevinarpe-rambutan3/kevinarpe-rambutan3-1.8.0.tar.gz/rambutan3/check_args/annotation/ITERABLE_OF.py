from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.iter.RIterableOfMatcher import RIterableOfMatcher
from rambutan3.check_args.seq.RSequenceOfMatcher import RSequenceOfMatcher


# noinspection PyPep8Naming
def ITERABLE_OF(type_matcher: RAbstractTypeMatcher) -> RSequenceOfMatcher:
    x = RIterableOfMatcher(type_matcher)
    return x
