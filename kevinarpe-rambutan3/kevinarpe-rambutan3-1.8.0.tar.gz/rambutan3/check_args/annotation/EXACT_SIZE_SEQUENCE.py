from rambutan3.check_args.seq.RRangeSizeSequenceMatcher import RRangeSizeSequenceMatcher
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum


# noinspection PyPep8Naming
def EXACT_SIZE_SEQUENCE(*, exact_size: int) -> RRangeSizeSequenceMatcher:
    x = RRangeSizeSequenceMatcher(RSequenceEnum.SEQUENCE, min_size=exact_size, max_size=exact_size)
    return x
