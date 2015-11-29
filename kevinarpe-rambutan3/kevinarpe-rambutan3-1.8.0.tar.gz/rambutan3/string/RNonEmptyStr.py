from rambutan3 import RArgs
from rambutan3.string.RStr import RStr


class RNonEmptyStr(RStr):
    """
    Subclass of {@link str} that guarantees its value is not empty (length > 0).

    This class is fully tested.

    @author Kevin Connor ARPE (kevinarpe@gmail.com)
    """

    def __init__(self, value: str):
        """
        @param value
               any non-empty string, including all whitespace, e.g., {@code " "} or {@code "\t"}

        @throws TypeError
                if {@code value} is not type {@link str}
        @throws ValueError
                if {@code value} has length zero
        """
        RArgs.check_is_instance(value, str, "value")
        if 0 == len(value):
            raise ValueError("Argument 'value' has length zero: '{}'".format(value))
        # This is bizarre.  Something is very special about str ctor.
        super().__init__()
