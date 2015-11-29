"""Base classes for value matching

@author Kevin Connor ARPE (kevinarpe@gmail.com)
"""
import inspect
import pprint

from abc import abstractmethod, ABC

from rambutan3 import RArgs
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError
from rambutan3.check_args.RCheckArgsError import RCheckArgsError
from rambutan3.error.RIllegalStateError import RIllegalStateError


# Ref: https://docs.python.org/3/library/abc.html#abc.abstractmethod
# Using this decorator requires that the class’s metaclass is ABCMeta or is derived from it.
class RAbstractTypeMatcher(ABC):
    """Abstract base class for all type matchers, include type matchers."""

    def __init__(self):
        raise NotImplementedError('Internal error: Do not call this constructor')

    @abstractmethod
    def matches(self, value, matcher_error: RTypeMatcherError=None) -> bool:
        """Tests if value matches

        Example: if matcher requires an instance of type {@code str}, then {@code "abc"} will return {@code True}.

        @param value
               value to test / match / check
        @param matcher_error
               None on first call.  If result is False, will be called again with non-None value.
               Matchers must:
               1) correctly update this object when traversing to sub-/child-matchers.
               2) correctly update this object when failing matches

        @return {@code True} if value matches, else {@code False}
        """
        raise NotImplementedError('Internal error: Do not call this member function')

    # RCheckArgsError.args[0] always holds a str message
    def check_arg(self, value, arg_name: str, *arg_name_format_args):
        """Checks if a value matches this matcher ({@code self})

        @param value
               reference to test
        @param arg_name
               name of argument to be used in thrown exception message, e.g., {@code "max_size"}
        @param *arg_name_format_args
               zero or more arguments passed to {@link str#format()} along with {@code arg_name}
               Example: if {@code arg_name} is {@code "Index {}"},
                        then {@code *arg_name_format_args} might be {@code 7}.
               Example: if {@code arg_name} is {@code "{}[{}]"},
                        then {@code *arg_name_format_args} might be {@code ("Index", 7)}.

        @return checked value

        @throws RCheckArgsError
                if {@link #matches()} fails
                e.args[0] always holds a str message
        """
        if self.matches(value):
            return value

        # Run again to capture the error.
        matcher_error = RTypeMatcherError()
        second_result = self.matches(value, matcher_error)

        formatted_arg_name = arg_name.format(*arg_name_format_args)

        # In theory, this should always be False, but let's check to be safe.
        if second_result:
            raise RIllegalStateError('Internal error: Second call to matches() passed'
                                     '\nvalue: [{}]'
                                     '\nformatted_arg_name: [{}]'
                                     '\nself: [{}]'
                                     .format(value, formatted_arg_name, self))

        traverse_path_str = matcher_error.traverse_path_str()
        formatted_arg_name += traverse_path_str

        # In this big ugly below, we are trying to format a beautiful error message.
        # Two broad paths:
        # (1) traverse_path_str is empty, so this is a top-level matcher failure
        # (2) traverse_path_str is not empty, so this is a child-level matcher failure
        # Why is this block of code so ugly and complicated?
        # We are trying create the most dense error message possible.  No waste / clutter.

        # Sample for (1):
        # rambutan3.check_args.RCheckArgsError.RCheckArgsError:
        # Argument name : bound2
        # Expected type : any value of {'<', '<='}
        # Expected type2: NoneType
        # Actual   type : str
        # Actual  value : '>'

        # Sample for (2):
        # rambutan3.check_args.RCheckArgsError.RCheckArgsError:
        # Argument name & path : arg_name_is_v['apps'][1]['name']
        # Expected child type  : str matching regex /^\s*\S+/ (human-readable message)
        # Actual   child type  : str
        # Actual   child value : ' '
        # Expected child type 2: str matching regex /^[A-Za-z_][0-9A-Za-z_]*$/ (identifier, e.g., ClassName or var_name3)
        # Actual   child type 2: str
        # Actual   child value2: ' '
        # Expected root  type : dict where EXACTLY {'apps': list where size >= 1 of [dict where EXACTLY {'name': str matching regex /^\s*\S+/ (human-readable message) | str matching regex /^[A-Za-z_][0-9A-Za-z_]*$/ (identifier, e.g., ClassName or var_name3), 'size': int where x > 0}]}
        # Actual   root  type : dict
        # Actual   root  value:
        # {'apps': [{'name': 'blah',
        #            'size': 123},
        #           {'name': ' ',
        #            'size': 123}]}

        if traverse_path_str:
            msg = "\nArgument name & path : {}".format(formatted_arg_name)
        else:
            msg = "\nArgument name : {}".format(formatted_arg_name)

        for index, failed_matcher_tuple in enumerate(matcher_error.failed_match_tuple_set_view):
            """:type failed_matcher_tuple: RTypeMatcherError.RFailedMatcherTuple"""
            failed_matcher = failed_matcher_tuple.matcher
            failed_value = failed_matcher_tuple.value
            formatted_failed_value = self._format_value(failed_value)
            optional_error_message = failed_matcher_tuple.optional_error_message
            num = ' ' if 0 == index else '{}'.format(1 + index)

            if traverse_path_str:
                msg += "\nExpected child type {}: {}" \
                       "\nActual   child type {}: {}" \
                       "\nActual   child value{}: {}" \
                       .format(num, failed_matcher,
                               num, type(failed_value).__name__,
                               num, formatted_failed_value)

                if optional_error_message:
                    msg += "\nMatcher error       : {}".format(optional_error_message)

            else:
                msg += "\nExpected type{}: {}".format(num, failed_matcher)

                if optional_error_message:
                    msg += "\nMatcher error{}: {}".format(num, optional_error_message)

        if traverse_path_str:
            formatted_value = self._format_value(value)
            msg += "\nExpected root  type : {}" \
                   "\nActual   root  type : {}" \
                   "\nActual   root  value: {}" \
                   .format(self,
                           type(value).__name__,
                           formatted_value)
        else:
            formatted_value = self._format_value(value)
            msg += "\nActual   type : {}" \
                   "\nActual  value : {}" \
                .format(type(value).__name__,
                        formatted_value)

        raise RCheckArgsError(msg)

    def _format_value(self, value):
        if inspect.isfunction(value):
            x = 'def {}{}'.format(value.__qualname__, inspect.signature(value))
        else:
            x = pprint.pformat(value)
            if '\n' in x:
                # This is a multi-line pformat(), then prepend another newline for readability.
                # width=1 is a trick to force pformat() to always format containers across multiple lines
                x = '\n' + pprint.pformat(value, width=1)

        return x

    # Advice: Do not override this method.  It will probably break later.
    def __or__(self, other):
        """operator|: Combines {@code self} with {@code other} to create logical OR type matcher

        @param other
               another type matcher

        @return new logical OR type matcher

        @see RLogicalOrValueMatcher
        """
        x = RLogicalOrTypeMatcher(self, other)
        return x

    @abstractmethod
    def __eq__(self, other) -> bool:
        """operator==: Compares {@code self} with {@code other}

        param other
              another type matcher

        @return False if {@code other} is not type {@code RAbstractTypeMatcher}
                Else, result of type matcher equality test

        """
        raise NotImplementedError('Internal error: Do not call this member function')

    # Advice: Do not override this method.  It will probably break later.
    # Accordingly, when defining __eq__(), one should also define __ne__()
    # so that the operators will behave as expected.
    # Ref: https://docs.python.org/3/reference/datamodel.html
    def __ne__(self, other) -> bool:
        x = not (self == other)
        return x

    @abstractmethod
    def __hash__(self) -> int:
        raise NotImplementedError('Internal error: Do not call this member function')

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError('Internal error: Do not call this member function')
        # TODO: Do impl next
        # x = self._core_str(0)

    # # TODO: Not sure about indent_level:int or indent:str
    # @abstractmethod
    # def _core_str2(self, indent_level: int) -> str:
    #     raise NotImplementedError('Internal error: Do not call this member function')


class RLogicalOrTypeMatcher(RAbstractTypeMatcher):
    """Combines two or more type matchers to create a unified logical OR type matcher

    This class is fully tested.
    """

    # noinspection PyMissingConstructor
    def __init__(self, left, right):
        """Never call this ctor directly; instead use operator|: {@link RValueMatcher#__or__()}

        @param left
               first type matcher; logical OR type matchers are handled correctly
        @param right
               second type matcher; logical OR type matchers are handled correctly

        @return new type matcher that combines first and second type matcher as logical OR type matcher
        """
        # Intentional: Do not call super(RAbstractTypeMatcher, self).__init__()
        RArgs.check_is_instance(left, RAbstractTypeMatcher, "left")
        RArgs.check_is_instance(right, RAbstractTypeMatcher, "right")

        matcher_list = []
        if isinstance(left, RLogicalOrTypeMatcher):
            matcher_list.extend(left.__matcher_tuple)
        else:
            matcher_list.append(left)

        if isinstance(right, RLogicalOrTypeMatcher):
            matcher_list.extend(right.__matcher_tuple)
        else:
            matcher_list.append(right)

        self.__matcher_tuple = tuple(matcher_list)
        self.__matcher_frozenset = frozenset(matcher_list)

    # @override
    def matches(self, value, matcher_error: RTypeMatcherError=None) -> bool:
        # Ref: http://stackoverflow.com/q/5217489/257299
        x = any(y.matches(value, matcher_error) for y in self.__matcher_tuple)
        return x

    def __iter__(self):
        """Iterates internal list of type matchers"""
        x = iter(self.__matcher_tuple)
        return x

    # @override
    def __eq__(self, other) -> bool:
        if not isinstance(other, RLogicalOrTypeMatcher):
            return False

        x = (self.__matcher_frozenset == other.__matcher_frozenset)
        return x

    # @override
    def __hash__(self) -> int:
        x = hash(self.__matcher_frozenset)
        return x

    # @override
    def __str__(self) -> str:
        x = " | ".join([str(x) for x in self.__matcher_tuple])
        return x
