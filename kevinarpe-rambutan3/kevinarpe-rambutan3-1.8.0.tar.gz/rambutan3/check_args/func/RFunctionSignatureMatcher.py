import inspect

from rambutan3 import RArgs, RTypes
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.RInstanceMatcher import RInstanceMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError


class RFunctionSignatureMatcher(RInstanceMatcher):

    def __init__(self, param_matcher_tuple: tuple, opt_return_matcher: RAbstractTypeMatcher=None):
        """
        :param param_matcher_tuple: list of RAbstractValueChecker
        :param opt_return_matcher: if None, this is a subroutine, not a function
        """
        super().__init__(*(RTypes.FUNCTION_TYPE_TUPLE))
        RArgs.check_not_none(param_matcher_tuple, "param_matcher_tuple")

        for index, param_matcher in enumerate(param_matcher_tuple):
            RArgs.check_is_instance(param_matcher, RAbstractTypeMatcher, "param_matcher_tuple[{}]", index)

        if opt_return_matcher is not None:
            RArgs.check_is_instance(opt_return_matcher, RAbstractTypeMatcher, "opt_return_matcher")

        self.__param_matcher_tuple = param_matcher_tuple
        self.__opt_return_matcher = opt_return_matcher

    # @override
    def matches(self, func: RTypes.FUNCTION_TYPE_TUPLE, matcher_error: RTypeMatcherError=None) -> bool:
        if not super().matches(func, matcher_error):
            return False

        sig = inspect.signature(func)
        """:type: Signature"""

        name_to_param_dict = sig.parameters
        """:type: dict[str, Parameter]"""

        result = (len(name_to_param_dict) == len(self.__param_matcher_tuple))

        if result:
            for index, param in enumerate(name_to_param_dict.values()):
                actual_matcher = param.annotation
                """:type: RAbstractTypeMatcher"""

                expected_matcher = self.__param_matcher_tuple[index]
                if expected_matcher != actual_matcher:
                    result = False
                    break

        if result:
            if (sig.return_annotation is not None) and (self.__opt_return_matcher is not None):
                result = (sig.return_annotation == self.__opt_return_matcher)
            else:
                # False if exactly one has return annotation.
                result = (sig.return_annotation is None) != (self.__opt_return_matcher is None)

        if not result and matcher_error:
            matcher_error.add_failed_match(self, func)

        return result

    # @override
    def __eq__(self, other) -> bool:
        if not isinstance(other, RFunctionSignatureMatcher):
            return False
        if not super().__eq__(other):
            return False
        x = (self.__opt_return_matcher == other.__opt_return_matcher
             and self.__param_matcher_tuple == other.__param_matcher_tuple)
        return x

    # @override
    def __hash__(self) -> int:
        # Ref: http://stackoverflow.com/questions/29435556/how-to-combine-hash-codes-in-in-python3
        super_hash = super().__hash__()
        self_hash = hash((self.__param_matcher_tuple, self.__opt_return_matcher))
        x = super_hash ^ self_hash
        return x

    # @override
    def __str__(self) -> str:
        args = " , ".join([str(pm) for pm in self.__param_matcher_tuple])
        x = "def *({})".format(args)
        if self.__opt_return_matcher:
            x += " -> {}".format(self.__opt_return_matcher)
        return x
