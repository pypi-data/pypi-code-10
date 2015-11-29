from rambutan3.check_args.seq.RRangeSizeSequenceMatcher import RRangeSizeSequenceMatcher
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum


# noinspection PyPep8Naming
def RANGE_SIZE_LIST(*, min_size: int=-1, max_size: int=-1) -> RRangeSizeSequenceMatcher:
    x = RRangeSizeSequenceMatcher(RSequenceEnum.LIST, min_size=min_size, max_size=max_size)
    return x
