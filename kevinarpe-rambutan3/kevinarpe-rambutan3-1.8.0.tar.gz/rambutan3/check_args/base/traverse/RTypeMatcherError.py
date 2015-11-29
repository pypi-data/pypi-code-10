from collections.abc import ValuesView
from collections import OrderedDict, namedtuple

from rambutan3 import RArgs
from rambutan3.check_args.base.traverse.RTypeMatcherTraversePathStep import RTypeMatcherTraversePathStep
from rambutan3.check_args.base.traverse.RTypeMatcherTraversePathStepEnum import RTypeMatcherTraversePathStepEnum
from rambutan3.error.RIllegalStateError import RIllegalStateError
from rambutan3.string.RMessageText import RMessageText


class RTypeMatcherError:

    RFailedMatcherTuple = namedtuple('RFailedMatcherTuple', ['matcher', 'value', 'optional_error_message'])

    def __init__(self):
        self.__reverse_step_list = []
        self.__failed_matcher_to_tuple_dict = OrderedDict()

    def add_traverse_path_step(self, step_type: RTypeMatcherTraversePathStepEnum, value):
        step = RTypeMatcherTraversePathStep(step_type, value)
        self.__reverse_step_list.append(step)

    @property
    def failed_match_tuple_set_view(self) -> ValuesView:
        if not self.__failed_matcher_to_tuple_dict:
            # TODO: TESTME
            raise RIllegalStateError('Internal error: Failed matches are unset')

        x = self.__failed_matcher_to_tuple_dict.values()
        return x

    def add_failed_match(self, matcher, value, error_message: RMessageText=None):
        """:type matcher: RAbstractTypeMatcher"""
        # ^^^ cannot import due to circular refs

        if error_message is not None:
            RArgs.check_is_instance(error_message, RMessageText, 'error_message')

        old_tuple = self.__failed_matcher_to_tuple_dict.get(matcher, None)

        if old_tuple:
            # TODO: TESTME
            if (old_tuple.value is not value) \
                or ((old_tuple.optional_error_message is not None)
                    and (old_tuple.optional_error_message != error_message)):

                raise RIllegalStateError('Internal error: Value is already set')

        self.__failed_matcher_to_tuple_dict[matcher] = \
            self.RFailedMatcherTuple(matcher=matcher, value=value, optional_error_message=error_message)

    def traverse_path_str(self) -> str:
        """
        @returns may be empty
        """
        x = ''.join([str(e) for e in reversed(self.__reverse_step_list)])
        return x
