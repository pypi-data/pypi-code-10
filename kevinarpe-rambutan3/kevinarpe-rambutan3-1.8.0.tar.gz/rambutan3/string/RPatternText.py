import inspect
from rambutan3 import RArgs, RTypes
from rambutan3.string.RMessageText import RMessageText
from rambutan3.string.RStr import RStr


class RPatternText(RStr):
    """
    Wraps a {@link str} value that matches a regular expression.

    Due to special constructor limitations with class {@link builtins#str}, do not call the constructor for this class
    directly.  Instead call @classmethod {@link #new()}.

    Examples: email address, telephone number, or postal code

    This class is fully tested.

    @author Kevin Connor ARPE (kevinarpe@gmail.com)
    """

    @classmethod
    def new(cls, value: str, regex_pattern: RTypes.REGEX_PATTERN_TYPE, human_readable_hint: RMessageText):
        """
        @param value
               any string that matches regular expression in {@code regex_pattern}
        @param regex_pattern
               regular expression to restrict valid string values
               do not forget to include begin and end anchors to match the entire string,
               e.g., {@code ^abc[def]ghi$}
        @param human_readable_hint
               describes the regular expression, e.g., 'Japanese postal code'

        @throws TypeError
                if {@code value} is not type {@link str}
                if {@code regex_pattern} is not a regular expression pattern
        @throws ValueError
                if {@code value} does not match regular expression in {@code regex_pattern}

        @see re#compile()
        """
        RArgs.check_is_instance(value, str, 'value')
        RArgs.check_is_instance(regex_pattern, RTypes.REGEX_PATTERN_TYPE, 'regex_pattern')
        RArgs.check_is_instance(human_readable_hint, RMessageText, 'human_readable_hint')
        if not regex_pattern.search(value):
            raise ValueError("Argument 'value' does not match regex /{}/ ({}): '{}'"
                             .format(regex_pattern.pattern, human_readable_hint, value))
        x = RPatternText(value)
        return x

    def __init__(self, value: str):
        """Do not call this ctor directly -- instead use {@link #new()}.

        @throws NotImplementedError
                if called directly
        """
        stack_list = inspect.stack()
        # 0, 1 -> to the correct stack frame
        # 0: This method
        # 1: new()
        caller_tuple = stack_list[1]
        caller_file = caller_tuple[1]
        caller_method_name = caller_tuple[3]
        if (caller_file != __file__) or ('new' != caller_method_name):
            raise NotImplementedError("Do not call this constructor directly -- instead use @classmethod new()")

        # This is bizarre.  Something is very special about str ctor.
        super().__init__()
