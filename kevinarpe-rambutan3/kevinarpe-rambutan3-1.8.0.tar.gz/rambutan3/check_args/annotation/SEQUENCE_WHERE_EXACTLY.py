from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum
from rambutan3.check_args.seq.RSequenceWhereMatcher import RSequenceWhereMatcher


# noinspection PyPep8Naming
def SEQUENCE_WHERE_EXACTLY(element_matcher_seq) -> RSequenceWhereMatcher:
    x = RSequenceWhereMatcher(RSequenceEnum.SEQUENCE, element_matcher_seq, is_exact=True)
    return x
