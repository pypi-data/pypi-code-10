import inspect

import types
import collections

from rambutan3 import RArgs
from rambutan3.check_args.RCheckArgsError import RCheckArgsError
from rambutan3.check_args.annotation.NONE import NONE
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.RInstanceMatcher import RInstanceMatcher
from rambutan3.check_args.cls_or_self.RClassInstanceMatcher import RClassInstanceMatcher
from rambutan3.check_args.cls_or_self.RSelfInstanceMatcher import RSelfInstanceMatcher

ParamTuple = collections.namedtuple('ParamTuple', ['param', 'type_matcher'])


class _RCheckArgsCallable:
    """Special internal class used by @check_args"""

    __FUNC_TYPE_TUPLE = (types.FunctionType, staticmethod, classmethod)

    def __init__(self, func: (types.FunctionType, staticmethod, classmethod)):
        RArgs.check_is_instance(func, self.__FUNC_TYPE_TUPLE, "func")
        if isinstance(func, (staticmethod, classmethod)):
            self.__unwrapped_func = getattr(func, '__func__')
        else:
            self.__unwrapped_func = func
        self.__func_signature = inspect.signature(self.__unwrapped_func)
        name_to_param_dict = self.__func_signature.parameters
        """:type: dict[str, Parameter]"""
        self.__param_tuple_list = []
        """:type: list[ParamTuple]"""
        for index, param in enumerate(name_to_param_dict.values()):
            """:type index: int"""
            """:type param: Parameter"""
            # Check param annotation
            if param.annotation is inspect.Parameter.empty:
                raise RCheckArgsError("Missing type annotation for parameter #{}: '{}'".format(1 + index, param.name))
            elif not isinstance(param.annotation, RAbstractTypeMatcher):
                raise RCheckArgsError("Parameter #{} '{}' annotation: Expected type '{}', but found type '{}'"
                                      .format(1 + index,
                                              param.name,
                                              RAbstractTypeMatcher.__name__,
                                              type(param.annotation).__name__))
            type_matcher = param.annotation
            """:type: RAbstractTypeMatcher"""
            # Check param default value
            if param.default is not inspect.Parameter.empty:
                type_matcher.check_arg(param.default, "Default value for argument #{} '{}': ", 1 + index, param.name)

            param_tuple = ParamTuple(param=param, type_matcher=type_matcher)
            self.__param_tuple_list.append(param_tuple)

        # Check return type
        if self.__func_signature.return_annotation is inspect.Signature.empty:
            self.__return_type_matcher = NONE
        elif isinstance(self.__func_signature.return_annotation, RAbstractTypeMatcher):
            self.__return_type_matcher = self.__func_signature.return_annotation
            """:type: RAbstractTypeMatcher"""
        else:
            raise RCheckArgsError("Return value annotation: Expected type '{}', but found type '{}'"
                                  .format(RAbstractTypeMatcher.__name__,
                                          type(self.__func_signature.return_annotation).__name__))
        self.__func = func

    def __call__(self, *args, **kwargs):
        try:
            bound_args = self.__func_signature.bind(*args, **kwargs)
        except TypeError as e:
            msg = "Failed to bind arguments: {}: {}".format(type(e).__name__, e)
            raise RCheckArgsError(msg) from e

        arg_num_offset = 1
        for param_index, param_tuple in enumerate(self.__param_tuple_list):
            type_matcher = param_tuple.type_matcher
            """:type: RAbstractTypeMatcher"""

            if isinstance(type_matcher, (RSelfInstanceMatcher, RClassInstanceMatcher)):
                # The first parameter for a method is always 'self',
                # but when calling a method, 'self' is passed implicitly.
                # The first parameter for a classmethod is always 'cls',
                # but when calling a method, 'cls' is passed implicitly.
                # Reduce the offset by one as first arg for method or classmethod will not be 'self' or 'cls'.
                # TODO: Allow SELF() and CLS() to have additional uses besides first argument.
                # Why?  Imagine __iadd__ for a special list class.  It might want to restrict incoming data to be the
                # same type as self.  It is a reasonable use case.
                arg_num_offset -= 1
                if 0 != param_index:
                    raise RCheckArgsError("SELF() and CLS() are only valid for first argument")
                if isinstance(type_matcher, RClassInstanceMatcher):
                    if not isinstance(self.__func, classmethod):
                        raise RCheckArgsError(
                            "CLS() is only valid for class methods (functions using @classmethod decorator)")
                    # The first argument ('cls') is never available here.  Continue with faith...
                    continue

            if param_tuple.param.name in bound_args.arguments:
                value = bound_args.arguments[param_tuple.param.name]
            elif param_tuple.param.default is not inspect.Parameter.empty:
                value = param_tuple.param.default
            else:
                # It may be impossible to hit this branch due to bind() call above.
                raise RCheckArgsError("Argument #{} ({}) is missing and has no default value"
                                      .format(param_index + arg_num_offset, param_tuple.param.name))

            # if inspect.Parameter.VAR_POSITIONAL == param_tuple.param.kind:
            #     value_tuple = value
            #     for value_index, value in enumerate(value_tuple):
            #         type_matcher.check_arg(value, "*{}[{}]: ", param_tuple.param.name, value_index)
            #
            # elif inspect.Parameter.VAR_KEYWORD == param_tuple.param.kind:
            #     key_value_dict = value
            #     for key, value in key_value_dict.items():
            #         type_matcher.check_arg(value, "**{}['{}']: ", param_tuple.param.name, key)
            # else:
            #     type_matcher.check_arg(value, param_tuple.param.name)

            # Disable old code above, which treated *args and **kwargs as special argument types.
            # Leaving the old code above for history.
            type_matcher.check_arg(value, param_tuple.param.name)

        result = self.__unwrapped_func(*args, **kwargs)

        self.__return_type_matcher.check_arg(result, "Return value: ")

        return result

    # Old obsolete code, but important for understanding stack crawling.
    # def _get_cls(self):
    #     # Python does not allow this code to run from __init__, so do it here.
    #     if not hasattr(self, '__cls'):
    #         module_name = self.__unwrapped_func.__module__
    #         module = importlib.import_module(module_name)
    #         # Ex: 'MyClass.my_classmethod'
    #         qual_name = self.__unwrapped_func.__qualname__
    #         name_list = qual_name.split('.')
    #
    #         # We need a for loop to handle nested classes, e.g., 'MyClass.MyNestedClass.my_classmethod'
    #         cls = module
    #         # Skip last item (method name)
    #         for name in name_list[:-1]:
    #             cls = getattr(cls, name)
    #
    #         self.__cls = cls
    #
    #     return self.__cls


def check_args(func: (types.FunctionType, staticmethod, classmethod, property)) -> types.FunctionType:
    """Function decorator for all types of functions:
    * Regular functions
    * Regular methods in classes
    * Class methods in classes (decorated with @classmethod)
    * Static methods in classes (decorated with @staticmethod)

    Each time the function is called, arguments are matched against parameter annotations.
    Mismatches are rejected and reported at runtime.

    Example function with return value:
    <pre>{@code
    @check_args
    def add(x: INT, y: INT) -> INT:
        return x + y
    }</pre>

    Example function without return value:
    <pre>{@code
    @check_args
    def foreach(data: NON_EMPTY_LIST, func: FUNC_OF(ANY).returnsNothing()):
        for x in data:
            func(x)
    }</pre>

    Optionally, for the above function, the return type matcher {@link NONE} may be used.  Surprisingly, all void Python
    functions return special singleton value {@code None} if, either, (a) no return statement exists, or (b) an empty
    return statement is used.  Some programming languages make the distinction between functions (with return types) and
    procedures (without return types).

    Example function witout return value, using {@code NONE} return type matcher:
    <pre>{@code
    @check_args
    def foreach(data: NON_EMPTY_LIST, func: FUNC_OF(ANY).returnsNothing()) -> NONE:
        for x in data:
            func(x)
    }</pre>

    Example regular method in class with zero explicit arguments:
    <pre>{@code
    class X:
        @check_args
        def get_data(self: SELF()) -> NON_EMPTY_TUPLE_OF(INT):
            return (1,2,3)
    }</pre>

    Example regular method in class with explicit arguments: (Order of @check_args and @classmethod is important!)
    <pre>{@code
    class X:
        @check_args
        def get_data(self: SELF(), data_tuple: TUPLE_OF(INT)=()) -> NON_EMPTY_TUPLE_OF(INT):
            return data_tuple + (1,2,3)
    }</pre>

    Example @classmethod with zero explicit arguments: (Order of @check_args and @classmethod is important!)
    <pre>{@code
    class X:
        @check_args
        @classmethod
        def get_data(cls: CLS()) -> NON_EMPTY_TUPLE_OF(INT):
            return (1,2,3)
    }</pre>

    Example @classmethod with explicit arguments: (Order of @check_args and @classmethod is important!)
    <pre>{@code
    class X:
        @check_args
        @classmethod
        def get_data(cls: CLS(), data_tuple: TUPLE_OF(INT)=()) -> NON_EMPTY_TUPLE_OF(INT):
            return data_tuple + (1,2,3)
    }</pre>

    Example @staticmethod with zero arguments: (Order of @check_args and @staticmethod is important!)
    <pre>{@code
    class X:
        @check_args
        @staticmethod
        def get_data() -> NON_EMPTY_TUPLE_OF(INT):
            return (1,2,3)
    }</pre>

    Example @staticmethod with arguments: (Order of @check_args and @staticmethod is important!)
    <pre>{@code
    class X:
        @check_args
        @staticmethod
        def add(x: NON_NEGATIVE_NUMBER, y: NON_NEGATIVE_NUMBER) -> NON_NEGATIVE_NUMBER:
            return x + y
    }</pre>

    Example @property: (Order of @check_args and @property is important!)
    <pre>{@code
    class X:
        @check_args
        @property
        def max_value(self: SELF()) -> POSITIVE_NUMBER:
            return self.__max_value
        }

        @check_args
        @max_value.setter
        def max_value(self: SELF(), value: POSITIVE_NUMBER) -> POSITIVE_NUMBER:
            old_value = self.__max_value
            self.__max_value = value
            return old_value
        }

        @check_args
        @max_value.deleter
        def max_value(self: SELF()) -> POSITIVE_NUMBER:
            last_value = self.__max_value
            del self.__max_value
            return last_value
    }</pre>

    Example property alternative: (Order of @check_args and @property is important!)
    <pre>{@code
    class X:
        @check_args
        def __get_max_value(self: SELF()) -> POSITIVE_NUMBER:
            return self.__max_value
        }

        @check_args
        def __set_max_value(self: SELF(), value: POSITIVE_NUMBER) -> POSITIVE_NUMBER:
            old_value = self.__max_value
            self.__max_value = value
            return old_value
        }

        @check_args
        def __del_max_value(self: SELF()) -> POSITIVE_NUMBER:
            last_value = self.__max_value
            del self.__max_value
            return last_value

        max_value = property(fget=__get_max_value, fset=__set_max_value, fdel=__del_max_value)
    }</pre>

    About *args
    ===========
    Zero or more variable positional arguments are captured by the * parameter prefix.
    This parameter may optionally be named, e.g., *args, *varArgs, *var_args.
    If unnamed, captured values are inaccessible.
    If named, values are captured as a tuple.

    Parameter annotations should use matchers:
        * TUPLE_OF()
        * NON_EMPTY_TUPLE_OF()
        * RANGE_SIZE_TUPLE_OF()

    About **kwargs
    ==============
    Zero or more variable keyword arguments are captured by the ** parameter prefix.
    This parameter may optionally be named, e.g., **kwargs, **varKeywordArgs, **var_keyword_args.
    If unnamed, captured values are inaccessible.
    If named, values are captured as a dict(ionary) with str keys.
    Note: The keys are always of type str!  It is not possible to capture non-str keys.
    Keys of non-str type will generate compile- or run-time errors.

    Parameter annotations should use matchers:
        * BUILTIN_DICT_OF()
        * NON_EMPTY_BUILTIN_DICT_OF()
        * RANGE_SIZE_BUILTIN_DICT_OF()
        * BUILTIN_DICT_WHERE_EXACTLY()
        * BUILTIN_DICT_WHERE_AT_LEAST()
    """
    if isinstance(func, property):
        x = __wrap_property(func)
    else:
        x = __wrap_func(func)
    return x


# Unlike functions, it is not possible to add arbitrary attributes to properties.
# Instead, use a set to track known, wrapped properties.
__WRAPPED_PROPERTY_SET = set()


def __wrap_property(prop: property) -> types.FunctionType:
    if prop in __WRAPPED_PROPERTY_SET:
        raise RCheckArgsError("Cannot apply same decorator twice")

    wrapped_fget = __wrap_property_func(prop.fget)
    wrapped_fset = __wrap_property_func(prop.fset)
    wrapped_fdel = __wrap_property_func(prop.fdel)
    wrapped_prop = property(fget=wrapped_fget, fset=wrapped_fset, fdel=wrapped_fdel, doc=prop.__doc__)
    __WRAPPED_PROPERTY_SET.add(wrapped_prop)
    return wrapped_prop


def __wrap_property_func(func: types.FunctionType) -> types.FunctionType:
    if (func is None) or hasattr(func, __CHECK_ARGS_ATTR_NAME):
        return func
    else:
        x = __wrap_func(func)
        return x


__CHECK_ARGS_ATTR_NAME = '__check_args__'


def __wrap_func(func: types.FunctionType) -> types.FunctionType:
    if hasattr(func, __CHECK_ARGS_ATTR_NAME):
        raise RCheckArgsError("Cannot apply same decorator twice")

    wrapped_func = _RCheckArgsCallable(func)

    # Why this additional layer of indirection?
    # A pure function does not eat special argument 'self'.
    # A functor (class that implements __call__()) will eat special argument 'self'.
    def check_args_delegator(*args, **kwargs):
        x = wrapped_func(*args, **kwargs)
        return x

    if isinstance(func, classmethod):
        check_args_delegator = classmethod(check_args_delegator)
    elif isinstance(func, staticmethod):
        check_args_delegator = staticmethod(check_args_delegator)

    setattr(check_args_delegator, '__doc__', func.__doc__)
    setattr(check_args_delegator, __CHECK_ARGS_ATTR_NAME, True)
    return check_args_delegator

# TODO: Move remaining items out

__TRACEBACK = RInstanceMatcher(types.TracebackType)


# noinspection PyPep8Naming
def TRACEBACK() -> RInstanceMatcher:
    return __TRACEBACK


__FRAME = RInstanceMatcher(types.FrameType)


# noinspection PyPep8Naming
def FRAME() -> RInstanceMatcher:
    return __FRAME

# __CAN_WRITE = RAttrMatcher(RTokenText("write"))
#
# def CAN_WRITE() -> RAttrMatcher:
#     return __CAN_WRITE
