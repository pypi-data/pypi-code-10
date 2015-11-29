from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum
from rambutan3.check_args.seq.RSequenceWhereMatcher import RSequenceWhereMatcher


# noinspection PyPep8Naming
def TUPLE_WHERE_AT_LEAST(element_matcher_seq) -> RSequenceWhereMatcher:
    x = RSequenceWhereMatcher(RSequenceEnum.TUPLE, element_matcher_seq, is_exact=False)
    return x
