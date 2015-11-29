from rambutan3 import RArgs
from rambutan3.check_args.base.RRestrictedInstanceMatcher import RRestrictedInstanceMatcher
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum


class RSequenceMatcher(RRestrictedInstanceMatcher):

    def __init__(self, seq_enum: RSequenceEnum):
        RArgs.check_is_instance(seq_enum, RSequenceEnum, "seq_enum")
        d = seq_enum.value
        """:type: RSequenceEnumData"""
        super().__init__(allowed_class_or_type_non_empty_tuple=d.allowed_type_tuple,
                         not_allowed_class_or_type_iterable=d.not_allowed_type_tuple)
