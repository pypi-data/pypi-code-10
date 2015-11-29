from rambutan3.check_args.annotation.FLOAT import FLOAT
from rambutan3.check_args.range.RNumberRangeMatcher import RNumberRangeMatcher


class RFloatRangeMatcher(RNumberRangeMatcher):

    def __init__(self, bound_op1: str, value1: float, bound_op2: str=None, value2: float=None):
        super().__init__(FLOAT, bound_op1, value1, bound_op2, value2)
