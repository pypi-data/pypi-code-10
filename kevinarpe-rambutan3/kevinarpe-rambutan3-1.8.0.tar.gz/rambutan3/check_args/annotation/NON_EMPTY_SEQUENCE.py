from rambutan3.check_args.seq.RRangeSizeSequenceMatcher import RRangeSizeSequenceMatcher
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum


NON_EMPTY_SEQUENCE = RRangeSizeSequenceMatcher(RSequenceEnum.SEQUENCE, min_size=1)
