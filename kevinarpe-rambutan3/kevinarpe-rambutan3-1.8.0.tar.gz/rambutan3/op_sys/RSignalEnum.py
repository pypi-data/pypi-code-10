import signal

from rambutan3.check_args.RCheckArgs import check_args
from rambutan3.check_args.annotation.CLS import CLS
from rambutan3.check_args.annotation.INSTANCE_BY_TYPE_NAME import INSTANCE_BY_TYPE_NAME
from rambutan3.check_args.annotation.INT import INT
from rambutan3.check_args.annotation.NONE import NONE
from rambutan3.enumeration.REnum import REnum

# Experimental: Used by rsubprocess.py
# Intentional!  Do not enable.
# @enum.unique
class RSignalEnum(REnum):
    SIGABRT = signal.SIGABRT
    SIGALRM = signal.SIGALRM
    SIGBUS = signal.SIGBUS
    SIGCHLD = signal.SIGCHLD
    SIGCLD = signal.SIGCLD
    SIGCONT = signal.SIGCONT
    SIGFPE = signal.SIGFPE
    SIGHUP = signal.SIGHUP
    SIGILL = signal.SIGILL
    SIGINT = signal.SIGINT
    SIGIO = signal.SIGIO
    SIGIOT = signal.SIGIOT
    SIGKILL = signal.SIGKILL
    SIGPIPE = signal.SIGPIPE
    SIGPOLL = signal.SIGPOLL
    SIGPROF = signal.SIGPROF
    SIGPWR = signal.SIGPWR
    SIGQUIT = signal.SIGQUIT
    SIGRTMAX = signal.SIGRTMAX
    SIGRTMIN = signal.SIGRTMIN
    SIGSEGV = signal.SIGSEGV
    SIGSTOP = signal.SIGSTOP
    SIGSYS = signal.SIGSYS
    SIGTERM = signal.SIGTERM
    SIGTRAP = signal.SIGTRAP
    SIGTSTP = signal.SIGTSTP
    SIGTTIN = signal.SIGTTIN
    SIGTTOU = signal.SIGTTOU
    SIGURG = signal.SIGURG
    SIGUSR1 = signal.SIGUSR1
    SIGUSR2 = signal.SIGUSR2
    SIGVTALRM = signal.SIGVTALRM
    SIGWINCH = signal.SIGWINCH
    SIGXCPU = signal.SIGXCPU
    SIGXFSZ = signal.SIGXFSZ

    # TODO: This is generic code.  Consider moving to REnum

    __VALUE_TO_MEMBER_DICT = None

    # TODO: Unused?  Need to use below?
    @classmethod
    def __value_to_member_dict(cls) -> dict:
        if cls.__VALUE_TO_MEMBER_DICT is None:
            cls.__VALUE_TO_MEMBER_DICT = \
                { enum_member.value: enum_member
                  # reversed?  Earlier enum members should have higher priority.
                  for name, enum_member in reversed([x for x in RSignalEnum._member_map_.items()]) }

        return cls.__VALUE_TO_MEMBER_DICT


    @check_args
    @classmethod
    def find_member_by_value(cls: CLS(), value: INT) -> INSTANCE_BY_TYPE_NAME('RSignalEnum'):
        member = cls.__VALUE_TO_MEMBER_DICT.get(value, None)
        if member is None:
            raise KeyError('Failed to find {} member for value: [{}]', type(RSignalEnum).__name__, value)
        return member


    @check_args
    @classmethod
    def try_find_member_by_value(cls: CLS(), value: INT) -> INSTANCE_BY_TYPE_NAME('RSignalEnum') | NONE:
        member = cls.__VALUE_TO_MEMBER_DICT.get(value, None)
        return member
