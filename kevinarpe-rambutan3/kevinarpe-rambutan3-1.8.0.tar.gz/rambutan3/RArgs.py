"""Simple argument checking functions

This module is fully tested.

@author Kevin Connor ARPE (kevinarpe@gmail.com)
"""


def check_not_none(value, arg_name: str, *arg_name_format_args):
    """Tests if a value is not none.

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

    @throws ValueError
            if {@code value} is {@code None}
    """
    if value is None:
        formatted_arg_name = arg_name.format(*arg_name_format_args)
        raise ValueError("Argument '{}' is None".format(formatted_arg_name))
    return value


def check_is_iterable(iterable, arg_name: str, *arg_name_format_args):
    """Tests if a value is iterable -- allows iter(iterable).

    As a special exception, any subclass of {@link builtins#str} is not considered iterable.
    Normally Python strings are iterable -- for each character.
    This feature is a topic of great debate within the Python community.
    While is it very difficult to remove the feature, it causes much grief in certain "duck typing" scenarios.

    @param iterable
           reference to test
    @param arg_name
           name of argument to be used in thrown exception message, e.g., {@code "data_list"}
    @param *arg_name_format_args
           zero or more arguments passed to {@link str#format()} along with {@code arg_name}
           Example: if {@code arg_name} is {@code "Index {}"},
                    then {@code *arg_name_format_args} might be {@code 7}.
           Example: if {@code arg_name} is {@code "{}[{}]"},
                    then {@code *arg_name_format_args} might be {@code ("Index", 7)}.

    @return checked iterable

    @throws TypeError
            if {@code iterable} is not iterable, including {@code None}
            SPECIAL CASE: if {@code iterable} is an instance of {@code str}
    """
    try:
        # No need for explicit None check; this will fail with None
        iter(iterable)
    except Exception as e:
        formatted_arg_name = arg_name.format(*arg_name_format_args)
        msg = "Argument '{}' of type '{}' is not iterable: '{}'\n\t{}"\
              .format(formatted_arg_name, type(iterable).__name__, iterable, e)
        raise TypeError(msg) from e

    if isinstance(iterable, str):
        formatted_arg_name = arg_name.format(*arg_name_format_args)
        raise TypeError("SPECIAL CASE: Argument '{}' of type '{}' is technically iterable, but not allowed: '{}'"
                        .format(formatted_arg_name, type(iterable).__name__, iterable))
    return iterable


def check_iterable_items_not_none(iterable, arg_name: str, *arg_name_format_args):
    """Tests if an iterable and all items are not {@code None}.

    An empty iterable will pass this test.

    @param iterable
           reference to test
    @param arg_name
           name of argument to be used in thrown exception message, e.g., {@code "file_name_list"}
    @param *arg_name_format_args
           zero or more arguments passed to {@link str#format()} along with {@code arg_name}
           Example: if {@code arg_name} is {@code "Index {}"},
                    then {@code *arg_name_format_args} might be {@code 7}.
           Example: if {@code arg_name} is {@code "{}[{}]"},
                    then {@code *arg_name_format_args} might be {@code ("Index", 7)}.

    @return checked iterable

    @throws TypeError
            if {@code iterable} is not iterable, including {@code None}
    @throws ValueError
            if any item from {@code iterable} is {@code None}

    @see #check_is_iterable()
    @see #check_iterable_not_empty()
    """
    check_is_iterable(iterable, arg_name, *arg_name_format_args)

    for index, value in enumerate(iterable):
        if value is None:
            formatted_arg_name = arg_name.format(*arg_name_format_args)
            raise ValueError("Iterable argument '{}[{}]' is None".format(formatted_arg_name, index))
    return iterable


__SENTINEL = object()


def check_iterable_not_empty(iterable, arg_name: str, *arg_name_format_args):
    """Tests if an iterable is not {@code None} and not empty

    @param iterable
           reference to test
    @param arg_name (str)
           name of argument to be used in thrown exception message, e.g., {@code "file_name_list"}
    @param *arg_name_format_args
           zero or more arguments passed to {@link str#format()} along with {@code arg_name}
           Example: if {@code arg_name} is {@code "Index {}"},
                    then {@code *arg_name_format_args} might be {@code 7}.
           Example: if {@code arg_name} is {@code "{}[{}]"},
                    then {@code *arg_name_format_args} might be {@code ("Index", 7)}.

    @return checked iterable

    @throws TypeError
            if {@code iterable} is not iterable, including {@code None}
    @throws ValueError
            if {@code iterable} is empty

    @see #check_is_iterable()
    @see #check_iterable_items_not_none()
    """
    check_is_iterable(iterable, arg_name)

    # Ref: http://stackoverflow.com/a/3114573/257299
    if __SENTINEL is next(iter(iterable), __SENTINEL):
        formatted_arg_name = arg_name.format(*arg_name_format_args)
        raise ValueError("Iterable argument '{}' is empty".format(formatted_arg_name))
    return iterable


def check_iterable_not_empty_and_items_not_none(iterable, arg_name: str, *arg_name_format_args):
    """Tests if an iterable is not {@code None}, not empty, and all items are not {@code None}.

    @param iterable
           reference to test
    @param arg_name (str)
           name of argument to be used in thrown exception message, e.g., {@code "file_name_list"}
    @param *arg_name_format_args
           zero or more arguments passed to {@link str#format()} along with {@code arg_name}
           Example: if {@code arg_name} is {@code "Index {}"},
                    then {@code *arg_name_format_args} might be {@code 7}.
           Example: if {@code arg_name} is {@code "{}[{}]"},
                    then {@code *arg_name_format_args} might be {@code ("Index", 7)}.

    @return checked iterable

    @throws TypeError
            if {@code iterable} is not iterable, including {@code None}
    @throws ValueError
            if {@code iterable} is empty or any item is {@code None}

    @see #check_iterable_not_empty()
    @see #check_iterable_items_not_none()
    """
    check_iterable_not_empty(iterable, arg_name, *arg_name_format_args)
    check_iterable_items_not_none(iterable, arg_name, *arg_name_format_args)
    return iterable


def check_is_instance(value, class_or_type_or_tuple_of: (type, tuple), arg_name: str, *arg_name_format_args):
    """Tests if a value is an instance of a type.

    Example: String value {@code "abc"} has type {@link builtins#str}.

    A value of {@code None} will pass this test if {@code class_or_type_or_tuple_of} is {@code type(None)}.

    @param value
           reference to test
    @param class_or_type_or_tuple_of
           class, type, or tuple of classes or types.  Must not be a list (or sequence).
    @param arg_name (str)
           name of argument to be used in thrown exception message, e.g., "file_name_list".
           May also be a {@link str#format()} string if arg_name is composed.
           Example: {@code "Index {}"}
           Example: {@code "{}[{}]"}
    @param *arg_name_format_args
           zero or more arguments passed to {@link str#format()} along with {@code arg_name}
           Example: if {@code arg_name} is {@code "Index {}"},
                    then {@code *arg_name_format_args} might be {@code 7}.
           Example: if {@code arg_name} is {@code "{}[{}]"},
                    then {@code *arg_name_format_args} might be {@code ("Index", 7)}.

    @return checked value

    @throws ValueError
            if {@code class_or_type_or_tuple_of} is {@code None}
    @throws TypeError
            if {@code class_or_type_or_tuple_of} is invalid, e.g., {@code "abc"}
            if {@code value} has unexpected type, e.g., "abc" for int, or 123 for str

    @see #isinstance()
    @see str#format()
    @see #check_not_none()
    """
    # We don't need to check if 'value' is None here.  Built-in function 'isinstance' will work with None.
    check_not_none(class_or_type_or_tuple_of, "class_or_type_or_tuple_of")

    try:
        # This will fail if class_or_type_or_tuple_of is something crazy like "abc"
        result = isinstance(value, class_or_type_or_tuple_of)
    except Exception as e:
        msg = "Argument 'class_or_type_or_tuple_of' is invalid: '{}'\n\t{}".format(class_or_type_or_tuple_of, e)
        raise TypeError(msg) from e

    if not result:
        formatted_arg_name = arg_name.format(*arg_name_format_args)
        if isinstance(class_or_type_or_tuple_of, tuple):
            x = "', '".join([type_.__name__ for type_ in class_or_type_or_tuple_of])
            x = "'" + x + "'"
            raise TypeError("Argument '{}': Expected any type of {}, but found value of type '{}': '{}'"
                            .format(formatted_arg_name, x, type(value).__name__, value))
        else:
            raise TypeError("Argument '{}': Expected type '{}', but found value of type '{}': '{}'"
                            .format(formatted_arg_name,
                                    class_or_type_or_tuple_of.__name__,
                                    type(value).__name__,
                                    value))
    return value


def check_iterable_items_is_instance(iterable,
                                     class_or_type_or_tuple_of: (type, tuple),
                                     arg_name: str, *arg_name_format_args):
    """Tests if items from an iterable are instances of a type.

    An empty iterable will pass this test.

    Example: Tuple {@code ("abc", "def")} has items of type {@link builtins#str}.

    @param iterable
           reference to test
    @param class_or_type_or_tuple_of
           class, type, or tuple of classes or types.  Must not be a list (or sequence).
    @param arg_name
           name of argument to be used in thrown exception message, e.g., {@code "file_name_list"}
    @param *arg_name_format_args
           zero or more arguments passed to {@link str#format()} along with {@code arg_name}
           Example: if {@code arg_name} is {@code "Index {}"},
                    then {@code *arg_name_format_args} might be {@code 7}.
           Example: if {@code arg_name} is {@code "{}[{}]"},
                    then {@code *arg_name_format_args} might be {@code ("Index", 7)}.

    @return checked iterable

    @throws ValueError
            if {@code class_or_type_or_tuple_of} is {@code None}
    @throws TypeError
            if {@code iterable} is not iterable, including {@code None}
            if {@code class_or_type_or_tuple_of} is invalid, e.g., {@code "abc"}
            if any item from {@code iterable} has unexpected type, e.g., "abc" for int, or 123 for str

    @see #check_is_iterable()
    @see #check_is_instance()
    """
    check_is_iterable(iterable, arg_name, *arg_name_format_args)
    for index, value in enumerate(iterable):
        # Optimisation: Do not call str.format() here.
        formatted_arg_name = arg_name + "[" + str(index) + "]"
        check_is_instance(value, class_or_type_or_tuple_of, formatted_arg_name, *arg_name_format_args)
    return iterable


def check_iterable_not_empty_and_items_is_instance(iterable,
                                                   class_or_type_or_tuple_of: (type, tuple),
                                                   arg_name: str,
                                                   *arg_name_format_args):
    """Tests if an iterable is not empty and items from an iterable are instances of a type.

    Example: Tuple {@code ("abc", "def")} has items of type {@link builtins#str}.

    @param iterable
           reference to test
    @param class_or_type_or_tuple_of
           class, type, or tuple of classes or types.  Must not be a list (or sequence).
    @param arg_name
           name of argument to be used in thrown exception message, e.g., {@code "file_name_list"}
    @param *arg_name_format_args
           zero or more arguments passed to {@link str#format()} along with {@code arg_name}
           Example: if {@code arg_name} is {@code "Index {}"},
                    then {@code *arg_name_format_args} might be {@code 7}.
           Example: if {@code arg_name} is {@code "{}[{}]"},
                    then {@code *arg_name_format_args} might be {@code ("Index", 7)}.

    @return checked iterable

    @throws ValueError
            if {@code iterable} is empty
            if {@code class_or_type_or_tuple_of} is {@code None}
    @throws TypeError
            if {@code iterable} is not iterable, including {@code None}
            if {@code class_or_type_or_tuple_of} is invalid, e.g., {@code "abc"}
            if any item from {@code iterable} has unexpected type, e.g., "abc" for int, or 123 for str

    @see #check_is_iterable()
    @see #check_is_instance()
    """
    check_iterable_not_empty(iterable, arg_name)
    for index, value in enumerate(iterable):
        # Optimisation: Do not call str.format() here.
        formatted_arg_name = arg_name + "[" + str(index) + "]"
        check_is_instance(value, class_or_type_or_tuple_of, formatted_arg_name, *arg_name_format_args)
    return iterable


def check_is_subclass(subclass: type, superclass: type, subclass_arg_name: str, *subclass_arg_name_format_args):
    """Tests if a type is a subclass of another type.

    If {@code subclass} and {@code superclass} are the same, this test will pass.

    @param subclass (type)
           type to test
    @param superclass (type)
           expected (super) type
    @param subclass_arg_name (str)
           name of argument to be used in thrown exception message, e.g., "file_handle_type".
    @param *subclass_arg_name_format_args
           zero or more arguments passed to {@link str#format()} along with {@code subclass_arg_name}
           Example: if {@code subclass_arg_name} is {@code "Index {}"},
           then {@code *arg_name_format_args} might be {@code 7}.

    @return checked subclass type

    @throws TypeError
            if {@code subclass} or {@code superclass} are not types, including {@code None}
            if type {@code subclass} is not a subclass of type {@code superclass}

    @see #issubclass()
    """
    check_is_instance(subclass, type, "subclass")
    check_is_instance(superclass, type, "superclass")

    if not issubclass(subclass, superclass):
        formatted_subclass_arg_name = subclass_arg_name.format(*subclass_arg_name_format_args)
        raise TypeError("Argument '{}': Expected subclass of type '{}', but found type '{}'"
                        .format(formatted_subclass_arg_name, superclass.__name__, subclass.__name__))
    return subclass


# def check_is_any_subclass(subclass, superclass_iterable, subclass_arg_name: str):
#     check_not_none(subclass, "subclass")
#     check_iterable_not_empty_and_items_not_none(superclass_iterable, "superclass_iterable")
#
#     for superclass in superclass_iterable:
#         if issubclass(subclass, superclass):
#             return subclass
#
#     x = "'" + "', '".join(superclass_iterable) + "'"
#     raise TypeError("Argument '{}': Expected any subclass of type '{}', but found type '{}'"
#                     .format(subclass_arg_name, x, subclass))
