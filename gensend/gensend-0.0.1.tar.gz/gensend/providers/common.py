import sys
import math
import operator
import string
from netaddr import IPNetwork, IPRange, IPGlob
from . import Provider


class WrappedPackages(Provider):
    WRAPPED = {
        operator: {
            None: ['eq', 'ne', 'gt', 'lt', 'ge', 'le'],
            str: ['concat'],
            int: ['add', 'sub', 'div', 'mul', 'mod'],
        },
        math: {
            float: ['ceil', 'fabs', 'factorial', 'floor', 'exp', 'expm1',
                    'log', 'pow', 'sqrt', 'degrees', 'radians'],
        },
        string: {
            str: ['lower', 'upper', 'capitalize', 'swapcase', 'translate',
                  'strip', 'lstrip', 'rstrip']
        }
    }

    def __init__(self):
        Provider.__init__(self)
        for src_object, src_targets in WrappedPackages.WRAPPED.items():
            for target_factories, target_names in src_targets.items():
                for target_name in target_names:
                    setattr(self, target_name, self._bind_func(
                        src_object, target_name, target_factories))


class WrappedFuncs(Provider):
    WRAPPED = {
        min: float,
        max: float,
    }

    def __init__(self):
        Provider.__init__(self)
        for src_func, src_factory in WrappedFuncs.WRAPPED.items():
            setattr(self, src_func.__name__, self._wrap_func(src_func, src_factory))


class Control(Provider, dict):
    def __init__(self):
        dict.__init__(self)
        Provider.__init__(self)
        self['if'] = self._dict_if
        self['repeat'] = self._dict_repeat

    def _dict_if(self, *args):
        """Returns the arguments in the list joined by STR.
            IF:CONDITION,DO,ELSE

        %{IF:False,'IS TRUE'} -> ''
        %{IF:True,'IS TRUE', 'NOT TRUE'} -> 'NOT TRUE'
        """
        call_args = list(args)
        do_cond = call_args.pop(0)
        do_if = call_args.pop(0)
        do_else = ''

        if len(call_args):
            do_else = call_args.pop()
        return do_if if self.truth(do_cond) else do_else

    def _dict_repeat(self, *args):
        """Do a thing N times
            REPEAT:N,DO

        %{REPEAT:10,%{INT}} -> '123 123 ... 123'
        """
        call_args = list(args)
        do_count = call_args.pop(0)
        do_thing = call_args.pop(0)
        do_out = []

        for i in range(int(do_count)):
            do_out.append(do_thing())
        return ''.join(do_out)

    def truth(self, *args):
        def to_truth(val):
            if isinstance(val, (list, tuple)):
                return len(val)
            return self.istrue(val)
        return all(self._arg_factory(to_truth, args))

    def pytruth(self, *args):
        """Performs a python truth value test. bool(arg), if multiple args are
        provided it will truth test them all.
            - https://docs.python.org/2/library/stdtypes.html#truth-value-testing
            PYTRUTH:1

        %{PYTRUTH:0} -> 'False'
        """
        return all(self._arg_factory(bool, args))

    def istrue(self, *args):
        """Strict test for 'true' value test. If multiple args are provided it will
        test them all.
            ISTRUE:true

        %{ISTRUE:true} -> 'True'
        """
        def is_true(val):
            if val is True:
                return True
            val = str(val).lower().strip()
            return val in ('true', 'yes', '1')
        return all(self._arg_factory(is_true, args))

    def isfalse(self, *args):
        def is_true(val):
            if val is False:
                return False
            val = str(val).lower().strip()
            return val in ('false', 'no', '0')
        return all(self._arg_factory(is_true, args))


class Common(Provider):
    """@TODO right now using an untrusted template could possible cause security
    issues the way that it's executed and not boxed in to a specific namespace"""

    def cr(self):
        """Prints carriage return
            \r

        %{LF} -> '\n'
        """
        return "\r"

    def lf(self):
        """Prints line feed
            \n

        %{LF} -> '\n'
        """
        return "\n"

    def crlf(self):
        """Prints carriage return and line feed
            NUL

        %{CRLF} -> '\r\n'
        """
        return "\r\n"

    def nul(self):
        """Prints a null byte
            NUL

        %{NUL} -> 'A'
        """
        return '\x00'

    def types(self, *args):
        """Used for debugging, returns type of each arg.
            TYPES,ARG_1,...,ARG_N

        %{TYPES:A,...,10} -> 'str(A) str(B) ... int(10)'
        """
        return ', '.join(['{0}({1})'.format(type(arg).__name__, arg) for arg in args])

    def join(self, *args):
        """Returns the arguments in the list joined by STR.
            FIRST,JOIN_BY,ARG_1,...,ARG_N

        %{JOIN: ,A,...,F} -> 'A B C ... F'
        """
        call_args = list(args)
        joiner = call_args.pop(0)
        self.random.shuffle(call_args)
        return joiner.join(call_args)

    def first(self, *args):
        """Returns the first value in the list.
            FIRST,ARG_1,...,ARG_N

        %{FIRST:A,...,F} -> 'A'
        """
        return args[0]

    def last(self, *args):
        """Returns the first value in the list.
            FIRST,ARG_1,...,ARG_N

        %{FIRST:A,...,F} -> 'F'
        """
        return args[-1]

    def shuffle(self, *args):
        """Shuffles all arguments and returns them.
            ARG_1,...,ARG_N

        %{SHUFFLE:A, B ,...,F} -> 'CDA B FE'
        """
        call_args = list(args)
        self.random.shuffle(call_args)
        return ''.join(call_args)

    def choice(self, *args):
        """Returns a random item from the arg list
            SEPARATOR,ARG_1,...,ARG_N

        %{CHOICE:A,...,F} -> 'B'
        """
        return self.random.choice(args)

    def float(self, *args):
        """Returns a random float between 0 and 1
            FLOAT

        %{FLOAT} -> '.1234567890'
        """
        return self.random.random()

    def ipglob(self, *args):
        """Returns a random address from within the given ip global
        https://pythonhosted.org/netaddr/api.html#ip-glob-ranges
            IPGLOB:GLOB

        %{IPGLOB:*.*.*.*} -> ''
        """
        call_args = list(args)
        return self.random.choice(IPGlob(call_args.pop(0)))

    def iprange(self, *args):
        """Returns a random address from within the given range of two addresses
            IPRANGE:start,end

        %{IPRANGE:10.0.0.0/8,} -> ''
        """
        call_args = list(args)
        return self.random.choice(IPRange(call_args.pop(0), call_args.pop(0)))

    def ipcidr(self, *args):
        """Returns a random address from within the given cidr notation
            IPCIDR:cidr

        %{IPCIDR:10.0.0.0/8} -> ''
        """
        call_args = list(args)
        return self.random.choice(IPNetwork(call_args.pop(0)))

    def int(self, *args):
        """Returns a random int between -sys.maxint and sys.maxint
            INT

        %{INT} -> '1245123'
        %{INT:10} -> '10000000'
        %{INT:10,20} -> '19'
        """
        return self.random.randint(*self._arg_defaults(args, [-sys.maxint, sys.maxint], int))
