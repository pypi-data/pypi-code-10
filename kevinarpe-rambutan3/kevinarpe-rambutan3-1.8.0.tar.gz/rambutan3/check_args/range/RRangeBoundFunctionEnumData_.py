import operator
import types

from rambutan3 import RArgs, RTypes


class RRangeBoundFunctionEnumData_:
    """This class exists only to be used by matchers."""

    # The first bound may be lower or upper; allow either.
    ONE_BOUND_OP_STR_SET = {'>', '>=', '<', '<='}
    TWO_BOUND_OP1_STR_SET = {'>', '>='}
    TWO_BOUND_OP2_STR_SET = {'<', '<='}

    @classmethod
    def check_bound_op_set_contains(cls, op_str: str, op_arg_name: str, op_str_set: set):
        RArgs.check_is_instance(op_str, str, op_arg_name)
        if op_str not in op_str_set:
            raise ValueError("Argument '{}': Expected one of {}, but found '{}'"
                             .format(op_arg_name, op_str_set, op_str))

    def __init__(self, op_str: str, op_func: RTypes.FUNCTION_TYPE_TUPLE):
        """:type op_func: types.FunctionType"""
        RArgs.check_is_instance(op_str, str, "op_str")
        self.check_bound_op_set_contains(op_str, "op_str", self.ONE_BOUND_OP_STR_SET)
        self.__op_str = op_str
        RArgs.check_is_instance(op_func, RTypes.FUNCTION_TYPE_TUPLE, "op_func")
        self.__op_func = op_func

    @property
    def op(self) -> str:
        return self.__op_str

    @property
    def op_func(self) -> types.FunctionType:
        return self.__op_func

    @property
    def is_greater(self) -> bool:
        x = (self.__op_func is operator.gt) or (self.__op_func is operator.ge)
        return x

    @property
    def is_inclusive(self) -> bool:
        x = (self.__op_func is operator.ge) or (self.__op_func is operator.le)
        return x

    def __eq__(self, other) -> bool:
        if not isinstance(other, RRangeBoundFunctionEnumData_):
            return False

        x = (self.__op_str == other.__op_str and self.__op_func == other.__op_func)
        return x

    def __hash__(self) -> int:
        x = hash((self.__op_str, self.__op_func))
        return x

    def __str__(self):
        return self.__op_str
