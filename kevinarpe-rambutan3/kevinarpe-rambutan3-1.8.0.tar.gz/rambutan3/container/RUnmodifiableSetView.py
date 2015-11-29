from rambutan3.container.RAbstractForwardingUnmodifiableSet import RAbstractForwardingUnmodifiableSet
from rambutan3.container.RSet import RSet
from rambutan3.check_args.RCheckArgs import check_args
from rambutan3.check_args.annotation.INSTANCE_OF import INSTANCE_OF
from rambutan3.check_args.annotation.SELF import SELF
from rambutan3.check_args.annotation.SET import SET


class RUnmodifiableSetView(RAbstractForwardingUnmodifiableSet):

    @check_args
    def __init__(self: SELF(), delegate_set: SET | INSTANCE_OF(RSet)):
        self.__set = delegate_set

    @property
    def _delegate(self) -> set:
        return self.__set
