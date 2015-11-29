from rambutan3.check_args.annotation.INT import INT
from rambutan3.check_args.range.RNumberRangeMatcher import RNumberRangeMatcher


class RIntRangeMatcher(RNumberRangeMatcher):

    def __init__(self, bound_op1: str, value1: int, bound_op2: str=None, value2: int=None):
        super().__init__(INT, bound_op1, value1, bound_op2, value2)
