from rambutan3.check_args.seq.RRangeSizeUniqueSequenceMatcher import RRangeSizeUniqueSequenceMatcher
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum


# noinspection PyPep8Naming
def RANGE_SIZE_UNIQUE_SEQUENCE(*, min_size: int=-1, max_size: int=-1) -> RRangeSizeUniqueSequenceMatcher:
    x = RRangeSizeUniqueSequenceMatcher(RSequenceEnum.SEQUENCE, min_size=min_size, max_size=max_size)
    return x
