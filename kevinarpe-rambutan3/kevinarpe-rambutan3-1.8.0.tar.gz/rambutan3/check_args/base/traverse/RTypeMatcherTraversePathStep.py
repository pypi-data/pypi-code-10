from rambutan3 import RArgs
from rambutan3.check_args.base.traverse.RTypeMatcherTraversePathStepEnum import RTypeMatcherTraversePathStepEnum
from rambutan3.string import RStrUtil


class RTypeMatcherTraversePathStep:

    def __init__(self, step_type: RTypeMatcherTraversePathStepEnum, value):
        RArgs.check_is_instance(step_type, RTypeMatcherTraversePathStepEnum, 'step_type')
        self.__step_type = step_type
        self.__value = value

    @property
    def step_type(self) -> RTypeMatcherTraversePathStepEnum:
        return self.__step_type

    @property
    def value(self):
        return self.__value

    # @override
    def __str__(self):
        x = RStrUtil.auto_quote(self.__value)
        # Both keys and indices are formatted similarly:
        # index 3   -> "[3]"
        # key 'abc' -> "['abc']"
        y = '[{}]'.format(x)
        return y
