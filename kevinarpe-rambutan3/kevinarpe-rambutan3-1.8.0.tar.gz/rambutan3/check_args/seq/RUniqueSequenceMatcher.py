from rambutan3.check_args.base.RAbstractForwardingTypeMatcher import RAbstractForwardingTypeMatcher
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum
from rambutan3.check_args.seq.RSequenceMatcher import RSequenceMatcher
from rambutan3.string import RStrUtil
from rambutan3.string.RMessageText import RMessageText


class RUniqueSequenceMatcher(RAbstractForwardingTypeMatcher):

    # noinspection PyMissingConstructor
    def __init__(self, seq_enum: RSequenceEnum):
        self.__delegate = RSequenceMatcher(seq_enum)

    @property
    def _delegate(self) -> RAbstractTypeMatcher:
        return self.__delegate

    # @override
    def matches(self, seq, matcher_error: RTypeMatcherError=None) -> bool:
        if not self.__delegate.matches(seq, matcher_error):
            return False

        x = self.core_matches(self, seq, matcher_error)
        return x

    @classmethod
    def core_matches(cls, self: RAbstractTypeMatcher, seq, matcher_error: RTypeMatcherError=None) -> bool:
        dupe_tuple_list = []
        value_set = set()
        for index, value in enumerate(seq):
            if value in value_set:
                dupe_tuple_list.append((index, value))
            else:
                value_set.add(value)

        if not dupe_tuple_list:
            return True

        if matcher_error:
            s = ', '.join(['({}: {})'.format(idx, RStrUtil.auto_quote(val)) for (idx, val) in dupe_tuple_list])
            m = 'Duplicates (index: value): ' + s
            matcher_error.add_failed_match(self, seq, RMessageText(m))

        return False

    # @override
    def __str__(self):
        x = "unique " + str(self.__delegate)
        return x
