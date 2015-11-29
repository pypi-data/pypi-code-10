from rambutan3.check_args.seq.RRangeSizeUniqueSequenceMatcher import RRangeSizeUniqueSequenceMatcher
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum


# noinspection PyPep8Naming
def NON_EMPTY_UNIQUE_TUPLE() -> RRangeSizeUniqueSequenceMatcher:
    x = RRangeSizeUniqueSequenceMatcher(RSequenceEnum.TUPLE, min_size=1)
    return x
