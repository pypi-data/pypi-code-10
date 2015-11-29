from rambutan3.container.RAbstractForwardingUnmodifiableList import RAbstractForwardingUnmodifiableList
from rambutan3.container.RList import RList
from rambutan3.check_args.RCheckArgs import check_args
from rambutan3.check_args.annotation.INSTANCE_OF import INSTANCE_OF
from rambutan3.check_args.annotation.SELF import SELF
from rambutan3.check_args.annotation.SEQUENCE import SEQUENCE


class RUnmodifiableListView(RAbstractForwardingUnmodifiableList):

    @check_args
    def __init__(self: SELF(), delegate_list: SEQUENCE | INSTANCE_OF(RList)):
        self.__list = delegate_list

    @property
    def _delegate(self) -> list:
        return self.__list
