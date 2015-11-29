import os

from rambutan3 import RArgs
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.RInstanceMatcher import RInstanceMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError
from rambutan3.op_sys.RFileAccessEnum import RFileAccessEnum
from rambutan3.op_sys.RFileTypeEnum import RFileTypeEnum
from rambutan3.string.RMessageText import RMessageText
from rambutan3 import ROpSysUtil


class RFilePathMatcher(RAbstractTypeMatcher):
    """This class is fully tested."""

    __STR_MATCHER = RInstanceMatcher(str)

    # noinspection PyMissingConstructor
    def __init__(self, file_type: RFileTypeEnum, *file_access_tuple: RFileAccessEnum):
        RArgs.check_is_instance(file_type, RFileTypeEnum, 'file_type')
        RArgs.check_iterable_not_empty_and_items_is_instance(file_access_tuple, RFileAccessEnum, 'file_access_tuple')
        self.__file_type = file_type
        self.__file_access_tuple = file_access_tuple

    # @override
    def matches(self, value: str, matcher_error: RTypeMatcherError=None) -> bool:
        if not self.__STR_MATCHER.matches(value, matcher_error):
            return False

        follow_symlinks = (RFileTypeEnum.SYMBOLIC_LINK != self.__file_type)
        try:
            stat_struct = os.stat(value, follow_symlinks=follow_symlinks)
        except Exception as e:
            if matcher_error:
                matcher_error.add_failed_match(self, value, RMessageText(repr(e)))

            return False

        stat_mode = stat_struct.st_mode
        stat_mode_file_type_test_func = self.__file_type.value[0]
        result = stat_mode_file_type_test_func(stat_mode)

        if not result and matcher_error:
            # Slow path: Report errors here
            self.__after_stat_mode_file_type_test_func_failed(value, matcher_error, stat_mode)

        if not result:
            return False

        result = ROpSysUtil.access(value, self.__file_access_tuple)

        if not result and matcher_error:
            # Slow path: Report errors here
            self.__after_test_access_failed(value, matcher_error)

        return result

    def __after_stat_mode_file_type_test_func_failed(self, value: str, matcher_error: RTypeMatcherError, stat_mode: int):
        found_flag = False
        for file_type in RFileTypeEnum:
            file_type_test_func = file_type.value[0]
            if file_type_test_func(stat_mode):
                m = RMessageText('Expected {}, but found {}'.format(self.__file_type, file_type))
                matcher_error.add_failed_match(self, value, m)
                found_flag = True
                break

        if not found_flag:
            matcher_error.add_failed_match(self, value, RMessageText('Internal error: Unknown file type'))

    def __after_test_access_failed(self, value: str, matcher_error: RTypeMatcherError):
        failed_mode_list = []
        for mode in self.__file_access_tuple:
            if not ROpSysUtil.access(value, mode):
                failed_mode_list.append(mode)

        m = RMessageText('Failed modes: ' + ', '.join([str(x) for x in failed_mode_list]))
        matcher_error.add_failed_match(self, value, m)

    # @override
    def __eq__(self, other) -> bool:
        if not isinstance(other, RFilePathMatcher):
            return False

        x = (self.__file_type == other.__file_type) \
            and (self.__file_access_tuple == other.__file_access_tuple)

        return x

    # @override
    def __hash__(self) -> int:
        x = hash((self.__file_type, self.__file_access_tuple))
        return x

    # @override
    def __str__(self):
        s = ', '.join([str(y.name) for y in self.__file_access_tuple])
        x = 'path to file of type {} with modes: {}'.format(self.__file_type.name, s)
        return x
