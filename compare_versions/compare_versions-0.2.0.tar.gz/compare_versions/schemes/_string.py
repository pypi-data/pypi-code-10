from .base import BaseScheme

class String(BaseScheme):
    """
    Performs naive string comparisons
    """
    def __init__(self, s):
        super(String, self).__init__(s)
