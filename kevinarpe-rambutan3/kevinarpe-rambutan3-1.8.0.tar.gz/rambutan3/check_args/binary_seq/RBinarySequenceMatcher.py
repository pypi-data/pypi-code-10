from rambutan3 import RArgs
from rambutan3.check_args.base.RInstanceMatcher import RInstanceMatcher
from rambutan3.check_args.binary_seq.RBinarySequenceEnum import RBinarySequenceEnum


class RBinarySequenceMatcher(RInstanceMatcher):

    def __init__(self, binary_seq_enum: RBinarySequenceEnum):
        RArgs.check_is_instance(binary_seq_enum, RBinarySequenceEnum, "binary_seq_enum")
        super().__init__(*(binary_seq_enum.value))
