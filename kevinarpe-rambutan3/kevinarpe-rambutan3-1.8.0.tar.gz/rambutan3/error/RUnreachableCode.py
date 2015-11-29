from rambutan3.error.RIllegalStateError import RIllegalStateError


class RUnreachableCode(RIllegalStateError):

    def __init__(self):
        super().__init__("Unreachable code")
