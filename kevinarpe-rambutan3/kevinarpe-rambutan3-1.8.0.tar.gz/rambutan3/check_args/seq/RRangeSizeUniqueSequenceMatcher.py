from rambutan3.check_args.base.RAbstractForwardingTypeMatcher import RAbstractForwardingTypeMatcher
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError
from rambutan3.check_args.seq.RRangeSizeSequenceMatcher import RRangeSizeSequenceMatcher
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum
from rambutan3.check_args.seq.RUniqueSequenceMatcher import RUniqueSequenceMatcher


class RRangeSizeUniqueSequenceMatcher(RAbstractForwardingTypeMatcher):

    # noinspection PyMissingConstructor
    def __init__(self, seq_enum: RSequenceEnum, *, min_size: int=-1, max_size: int=-1):
        self.__delegate = RRangeSizeSequenceMatcher(seq_enum, min_size=min_size, max_size=max_size)

    @property
    def _delegate(self) -> RAbstractTypeMatcher:
        return self.__delegate

    # @override
    def matches(self, seq, matcher_error: RTypeMatcherError=None) -> bool:
        if not self.__delegate.matches(seq, matcher_error):
            return False

        x = RUniqueSequenceMatcher.core_matches(self, seq, matcher_error)
        return x

    # @override
    def __str__(self):
        x = "unique " + str(self.__delegate)
        return x
