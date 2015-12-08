class BaseScheme(object):
    """
    Base class for versioning schemes
    """

    def __init__(self, comparable, printable=None):
        """
        Arguments:
        comparable -- some object which can be compared to other objects of the same type
        printable -- a printable representation of the verison
        """
        self._c = comparable
        if printable is None:
            self._p = comparable
        else:
            self._p = printable

    # Representations

    def __str__(self):
        return str(self._p)
    def __repr__(self):
        return repr(self._p)

    # Comparison operators

    def __eq__(self, other):
        self.check_type(other)
        return self._c == other._c
    def __gt__(self, other):
        self.check_type(other)
        return self._c > other._c
    def __lt__(self, other):
        self.check_type(other)
        return self._c < other._c
    def __ne__(self, other):
        return not self == other
    def __ge__(self, other):
        return self == other or self > other
    def __le__(self, other):
        return self == other or self < other

    # Other functions

    def check_type(self, other):
        """
        Asserts that the version to be compared is of the same type
        """
        assert type(self) == type(other)

