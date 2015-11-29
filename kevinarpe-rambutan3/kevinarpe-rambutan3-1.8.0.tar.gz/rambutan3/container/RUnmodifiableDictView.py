from rambutan3.container.RDict import RDict
from rambutan3.container.RAbstractForwardingUnmodifiableDict import RAbstractForwardingUnmodifiableDict
from rambutan3.check_args.RCheckArgs import check_args
from rambutan3.check_args.annotation.DICT import DICT
from rambutan3.check_args.annotation.INSTANCE_OF import INSTANCE_OF
from rambutan3.check_args.annotation.SELF import SELF


class RUnmodifiableDictView(RAbstractForwardingUnmodifiableDict):

    @check_args
    def __init__(self: SELF(), delegate_dict: DICT | INSTANCE_OF(RDict)):
        self.__dict = delegate_dict

    @property
    def _delegate(self) -> dict:
        return self.__dict
