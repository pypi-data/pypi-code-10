import re

from rambutan3 import RArgs
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError
from rambutan3.check_args.file.RFilePathTypeEnum import RFilePathTypeEnum
from rambutan3.check_args.other.RRegexMatcher import RRegexMatcher
from rambutan3.string.RMessageText import RMessageText


class RUncheckedRestrictedUnixFilePathMatcher(RAbstractTypeMatcher):
    """This class is fully tested."""


    # By design, root ('/') is not allowed.
    # Why?  I cannot think when this will ever be required in general programming.
    # It is probably a mistake... like iterating the characters of a string!

    # Allowed:
    # 'abc'
    # 'abc/'
    # 'abc/.'
    # 'abc/..'
    # '/abc'
    # './abc'
    # '../abc'
    # '/abc/'
    # './abc/'
    # '../abc/'
    # '/abc/.'
    # '/abc/..'
    # './abc/.'
    # '../abc/..'
    # './abc/..'
    # '../abc/.'
    # ...........................
    # 'abc/def'
    # 'abc/def/'
    # '/abc/def'
    # '/abc/def/'
    # '/abc/def'
    # '/abc/def/'
    # Not allowed: Any str containing '//'

    __REGEX_MATCHER = RRegexMatcher(re.compile(r'^[A-Za-z0-9_\-\.=/]+$'), RMessageText('restricted UNIX file path'))

    # noinspection PyMissingConstructor
    def __init__(self, *allowed_file_path_type_tuple: RFilePathTypeEnum):
        RArgs.check_iterable_not_empty_and_items_is_instance(allowed_file_path_type_tuple,
                                                             RFilePathTypeEnum,
                                                             'allowed_file_path_type_tuple')
        self.__allowed_file_path_type_frozenset = frozenset(allowed_file_path_type_tuple)

    # @override
    def matches(self, value: str, matcher_error: RTypeMatcherError=None) -> bool:
        if not self.__REGEX_MATCHER.matches(value, matcher_error):
            return False

        result = '//' not in value

        if not result and matcher_error:
            matcher_error.add_failed_match(self, value, RMessageText('Contains "//"'))

        if not result:
            return False

        for file_path_enum in self.__allowed_file_path_type_frozenset:
            file_path_enum_test_func = file_path_enum.value[0]
            if file_path_enum_test_func(value):
                return True

        if matcher_error:
            j = self.__join_allowed_file_path_type_frozenset()
            m = RMessageText('Expected ' + j)
            matcher_error.add_failed_match(self, value, m)

        return False

    def __join_allowed_file_path_type_frozenset(self):
        x = ' or '.join([x.name for x in self.__allowed_file_path_type_frozenset])
        return x

    # @override
    def __eq__(self, other) -> bool:
        if not isinstance(other, RUncheckedRestrictedUnixFilePathMatcher):
            return False

        x = (self.__allowed_file_path_type_frozenset == other.__allowed_file_path_type_frozenset)
        return x

    # @override
    def __hash__(self) -> int:
        x = hash(self.__allowed_file_path_type_frozenset)
        return x

    # @override
    def __str__(self):
        j = self.__join_allowed_file_path_type_frozenset()
        x = 'str matching restricted UNIX file path pattern ({})'.format(j)
        return x
