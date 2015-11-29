from rambutan3.check_args.seq.RRangeSizeUniqueSequenceMatcher import RRangeSizeUniqueSequenceMatcher
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum


# noinspection PyPep8Naming
def EXACT_SIZE_UNIQUE_SEQUENCE(*, exact_size: int) -> RRangeSizeUniqueSequenceMatcher:
    x = RRangeSizeUniqueSequenceMatcher(RSequenceEnum.SEQUENCE, min_size=exact_size, max_size=exact_size)
    return x
