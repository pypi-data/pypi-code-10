from rambutan3 import RArgs
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError
from rambutan3.check_args.base.traverse.RTypeMatcherTraversePathStepEnum import RTypeMatcherTraversePathStepEnum
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum
from rambutan3.check_args.seq.RSequenceMatcher import RSequenceMatcher
from rambutan3.string import RStrUtil
from rambutan3.string.RMessageText import RMessageText


class RSequenceWhereMatcher(RAbstractTypeMatcher):

    # noinspection PyMissingConstructor
    def __init__(self, seq_enum: RSequenceEnum, element_matcher_seq, *, is_exact: bool):
        self.__seq_matcher = RSequenceMatcher(seq_enum)
        RArgs.check_iterable_not_empty_and_items_is_instance(element_matcher_seq,
                                                             RAbstractTypeMatcher,
                                                             "element_matcher_seq")
        RArgs.check_is_instance(is_exact, bool, "is_exact")

        self.__element_matcher_tuple = tuple(element_matcher_seq)
        """:type: tuple[RAbstractTypeMatcher]"""
        self.__is_exact = is_exact

    # @override
    def matches(self, seq, matcher_error: RTypeMatcherError=None) -> bool:
        if not self.__seq_matcher.matches(seq, matcher_error):
            return False

        actual_size = len(seq)
        expected_size = len(self.__element_matcher_tuple)

        # We have two types of 'WhereMatcher's: WhereExactly and WhereAtLeast.
        # Always too few items is wrong.
        if actual_size < expected_size:
            if matcher_error:
                matcher_error.add_failed_match(self, seq, RMessageText("Actual size is {}".format(actual_size)))

            return False

        for index, (element_matcher, value) in enumerate(zip(self.__element_matcher_tuple, seq)):
            if not element_matcher.matches(value, matcher_error):
                if matcher_error:
                    matcher_error.add_traverse_path_step(RTypeMatcherTraversePathStepEnum.Index, index)

                return False

        if self.__is_exact and actual_size > len(self.__element_matcher_tuple):
            if matcher_error:
                extra_items_seq_slice = seq[actual_size:]
                m = RMessageText('Extra items: {}'.format(extra_items_seq_slice))
                matcher_error.add_failed_match(self, seq, m)

            return False

        return True

    # @override
    def __eq__(self, other) -> bool:
        if not isinstance(other, RSequenceWhereMatcher):
            return False

        if not self.__seq_matcher == other.__seq_matcher:
            return False

        x = ((self.__element_matcher_tuple == other.__element_matcher_tuple)
             and (self.__is_exact == other.__is_exact))
        return x

    # @override
    def __hash__(self) -> int:
        x = hash((self.__seq_matcher, self.__element_matcher_tuple, self.__is_exact))
        return x

    # @override
    def __str__(self):
        where_clause = "EXACTLY" if self.__is_exact else "AT LEAST"
        s = RStrUtil.auto_quote_tuple(self.__element_matcher_tuple)
        x = "{} where {} {}".format(self.__seq_matcher, where_clause, s)
        return x
