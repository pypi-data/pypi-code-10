####################################################
## Scheme in Python
##
## Jim Marshall
## Doug Blank
####################################################


#############################################################
# Scheme.py
# These are native implementations of functions to allow
# the register machine translation to run in Python

from __future__ import division, print_function

from collections import Iterable
import inspect
import fractions
import functools
import operator
import types
import math
import time
import sys
import os

PY3 = sys.version_info[0] == 3

#############################################################
# Python implementation notes:
#
# Each symbol is a singleton for easy comparison reasons:
# Symbol("x") is Symbol("x")
#
# Python's list is used as Scheme's vector.
#
# The List() class is used for Scheme's con-cell based lists.
#
# Lists implement iter, so you can use Python's iter tools
# (such as [x for x in List(1, 2, 3)])
#
# A couple of functions are O(2n) because they have a 
# reverse. Should be fixed to be O(n).
#############################################################

## Global symbols:

# Set to a dictionary-like object for global-shared namespace:
ENVIRONMENT = {}
# Python environment:
if "str" in dir(__builtins__):
    ENVIRONMENT.update({key: getattr(__builtins__, key) 
                        for key in dir(__builtins__)})
# IPython environment:
if "keys" in dir(__builtins__):
    ENVIRONMENT.update(__builtins__)
ENVIRONMENT["DEBUG"] = False

GLOBALS = globals()

class DebugException(Exception):
    """
    Exception for use in GUI
    """
    def __init__(self, data):
        super(DebugException, self).__init__()
        self.data = data

class Char(object):
    def __init__(self, c):
        self.char = c
    def __eq__(self, other):
        return isinstance(other, Char) and self.char == other.char
    def __lt__(self, other):
        return isinstance(other, Char) and self.char < other.char
    def __gt__(self, other):
        return isinstance(other, Char) and self.char > other.char
    def __str__(self):
        if self.char == " ":
            return "#\\space"
        elif self.char == "\n":
            return "#\\newline"
        return "#\\%s" % self.char
    def __repr__(self):
        return str(self)

class Symbol(object):
    def __init__(self, name):
        self.name = name
        self.hash = hash(name)

    def __repr__(self):
        return "%s" % self.name

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.hash == other.hash

    def __hash__(self):
        return hash(self.name)

    def __iter__(self):
        # So that EmptyList will be treated as []
        return self

    def next(self):
        # So that EmptyList will be treated as []
        raise StopIteration

    def __next__(self):
        # So that EmptyList will be treated as []
        raise StopIteration

    def __len__(self):
        # So that EmptyList will be treated as []
        return 0

    def __getattr__(self, attr):
        if attr == "name":
            return self.__getattribute__("name")
        elif hasattr(self.name, attr):
            return getattr(self.name, attr)
        else:
            raise AttributeError("no such attribute '%s' on '%s'" % (attr, self.name))

SYMBOLS = {}
CHARS = {}

def make_symbol(string):
    if not (string in SYMBOLS):
        SYMBOLS[string] = Symbol(string)
    return SYMBOLS[string]

def make_char(c):
    if not (c in CHARS):
        CHARS[c] = Char(c)
    return CHARS[c]

void_value = make_symbol("<void>")

def make_initial_env_extended(names, procs, docstrings):
    ## If you wish to extend the environment to 
    ## include native values, do so here:
    return make_initial_environment(names, procs, docstrings)

### Lists:

class cons(object):
    # build a cons cell
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

    def __repr__(self):
        # Written to not deal with exact same
        # atoms, so will work with unpickled objs
        if isinstance(self.car, Symbol):
            if self.car.name == "procedure":
                return "#<procedure>"
            elif self.car.name == "environment":
                return "#<environment>"
        retval = ""
        current = self
        while isinstance(current, cons):
            if retval:
                retval += " "
            retval += make_safe(current.car)
            current = current.cdr
        if not (isinstance(current, Symbol) and current.name == "()"):
            retval += " . " + make_safe(current)
        return "(%s)" % retval

    def __call__(self, *args, **kwargs):
        if self.car is symbol_procedure:
            return dlr_func(self)(*args, **kwargs)
        else:
            raise Exception("not a procedure")

    def __iter__(self):
        cp = cons(self.car, self.cdr)
        cp.current = cp
        return cp

    def __len__(self):
        if isinstance(self.cdr, cons):
            current = self
            count = 0
            while isinstance(current, cons):
                count += 1
                current = current.cdr
            if null_q(current):
                return count
            else:
                raise AttributeError("list is not a proper list")
        else:
            return 1

    def next(self): # Python 2
        if not isinstance(self.current, cons):
            raise StopIteration
        else:
            retval = self.current.car
            self.current = self.current.cdr
            return retval

    def __next__(self): # Python 3
        if not isinstance(self.current, cons):
            raise StopIteration
        else:
            retval = self.current.car
            self.current = self.current.cdr
            return retval

    def __getitem__(self, pos):
        ls = list(self)
        return ls[pos]

def List(*args):
    # Scheme list
    retval = symbol_emptylist
    i = 0
    while i < len(args):
        arg = args[len(args) - i - 1]
        retval = cons(arg, retval)
        i += 1
    return retval

def reverse(lyst):
    retval = symbol_emptylist
    current = lyst
    while isinstance(current, cons):
        retval = cons(current.car, retval)
        current = current.cdr
    if current != symbol_emptylist:
        raise Exception("not a proper list")
    return retval

def length(lyst):
    current = lyst
    count = 0
    while isinstance(current, cons):
        current = current.cdr
        count += 1
    if current != symbol_emptylist:
        raise Exception("not a proper list")
    return count

def Map(f, lyst, lyst2=None):
    if lyst2 is None:
        retval = symbol_emptylist
        current = lyst
        while isinstance(current, cons):
            retval = cons(f(current.car), retval)
            current = current.cdr
        if current != symbol_emptylist:
            raise Exception("not a proper list")
        # FIXME: rewrite without reverse
        return reverse(retval)
    else:
        retval = symbol_emptylist
        current1 = lyst
        current2 = lyst2
        while isinstance(current1, cons) and isinstance(current2, cons):
            retval = cons(f(current1.car, current2.car), retval)
            current1 = current1.cdr
            current2 = current2.cdr
        if current1 != symbol_emptylist:
            raise Exception("not a proper list")
        if current2 != symbol_emptylist:
            raise Exception("not a proper list")
        # FIXME: rewrite without reverse
        return reverse(retval)

def for_each(f, lyst):
    current = lyst
    while isinstance(current, cons):
        f(current.car)
        current = current.cdr
    if current != symbol_emptylist:
        raise Exception("not a proper list")

def pivot (p, l):
    if null_q(l):
        return make_symbol("done")
    elif null_q(cdr(l)):
        return make_symbol("done")
    result = apply_comparison(p, car(l), cadr(l))
    if result:
        return pivot(p, cdr(l))
    else:
        return car(l)

def make_comparison_function(procedure):
    # FIXME: should rewrite this using CPS style
    def compare(carl, cadrl):
        GLOBALS["save_k2_reg"] = k2_reg
        GLOBALS["proc_reg"] = procedure
        GLOBALS["args_reg"] = List(carl, cadrl)
        GLOBALS["handler_reg"] = REP_handler
        GLOBALS["k2_reg"] = REP_k
        GLOBALS["pc"] = apply_proc
        retval = trampoline()
        GLOBALS["k2_reg"] = save_k2_reg
        return retval
    return compare

def apply_comparison(p, carl, cadrl):
    return p(carl, cadrl)

## usage: (partition 4 '(6 4 2 1 7) () ()) -> returns partitions
def partition (p, piv, l, p1, p2):
    if (null_q(l)):
        return List(p1, p2)
    result = apply_comparison(p, car(l), piv)
    if (result):
        return partition(p, piv, cdr(l), cons(car(l), p1), p2)
    else:
        return partition(p, piv, cdr(l), p1, cons(car(l), p2))

def sort(p, l):
    # FIXME: should rewrite this using CPS style
    # in order to use CPS comparison operators
    if procedure_q(p):
        f = make_comparison_function(p)
    else:
        f = p
    piv = pivot(f, l)
    if (piv is make_symbol("done")): return l
    parts = partition(f, piv, l, symbol_emptylist, symbol_emptylist)
    return append(sort(f, car(parts)),
                  sort(f, cadr(parts)))

def append(*objs):
    retval = objs[-1]
    # FIXME: rewrite without reversed
    for obj in reversed(objs[:-1]):
        # FIXME: rewrite without reverse
        current = reverse(obj)
        while isinstance(current, cons):
            retval = cons(current.car, retval)
            current = current.cdr
    return retval

def car(lyst):
    return lyst.car

def cdr(lyst):
    return lyst.cdr

def caar(lyst):
    return lyst.car.car

def cadr(lyst):
    return lyst.cdr.car

def cddr(lyst):
    return lyst.cdr.cdr

def cdar(lyst):
    return lyst.car.cdr

def caddr(lyst):
    return lyst.cdr.cdr.car

def cadar(lyst):
    return lyst.car.cdr.car

def cdddr(lyst):
    return lyst.cdr.cdr.cdr

def cadddr(lyst):
    return lyst.cdr.cdr.cdr.car

def cddddr(lyst):
    return lyst.cdr.cdr.cdr.cdr

def caaaar(lyst):
    return lyst.car.car.car.car

def caaadr(lyst):
    return lyst.cdr.car.car.car

def caaar(lyst):
    return lyst.car.car.car

def caadar(lyst):
    return lyst.car.cdr.car.car

def caaddr(lyst):
    return lyst.cdr.cdr.car.car

def caadr(lyst):
    return lyst.cdr.car.car

def cadaar(lyst):
    return lyst.car.car.cdr.car

def cadadr(lyst):
    return lyst.cdr.car.cdr.car

def caddar(lyst):
    return lyst.car.cdr.cdr.car

def cdaaar(lyst):
    return lyst.car.car.car.cdr

def cdaadr(lyst):
    return lyst.cdr.car.car.cdr

def cdaar(lyst):
    return lyst.car.car.cdr

def cdadar(lyst):
    return lyst.car.cdr.car.cdr

def cdaddr(lyst):
    return lyst.cdr.cdr.car.cdr

def cdadr(lyst):
    return lyst.cdr.car.cdr

def cddaar(lyst):
    return lyst.car.car.cdr.cdr

def cddadr(lyst):
    return lyst.cdr.car.cdr.cdr

def cddar(lyst):
    return lyst.car.cdr.cdr

def cdddar(lyst):
    return lyst.car.cdr.cdr.cdr

def set_car_b(cell, item):
    cell.car = item
    return void_value

def set_cdr_b(cell, item):
    cell.cdr = item
    return void_value

def list_tail(lyst, pos):
    if pos < 0:
        raise Exception("invalid list-ref position: " + pos)
    current = lyst
    while pos != 0:
        current = current.cdr
        pos = pos - 1
    return current

def list_head(lyst, pos):
    retval = symbol_emptylist
    current = lyst
    while pos != 0:
        retval = cons(current.car, retval)
        current = current.cdr
        pos = pos - 1
    # FIXME: rewrite without reverse
    return reverse(retval)

def list_ref(lyst, pos):
    if pos < 0:
        raise Exception("invalid list-ref position: " + pos)
    current = lyst
    while pos != 0:
        current = current.cdr
        pos = pos - 1
    return current.car

def vector_length(vec):
    return len(vec)

### Native make- functions:

def make_proc(*args):
    return List(symbol_procedure, *args)

def make_macro(*args):
    return List(symbol_macro_transformer, *args)

def make_cont(*args):
    return List(symbol_continuation, *args)

def make_cont2(*args):
    return List(symbol_continuation2, *args)

def make_cont3(*args):
    return List(symbol_continuation3, *args)

def make_cont4(*args):
    return List(symbol_continuation4, *args)

def make_fail(*args):
    return List(symbol_fail_continuation, *args)

def make_handler(*args):
    return List(symbol_handler, *args)

def make_handler2(*args):
    return List(symbol_handler2, *args)

### Native other functions:

def length_one_q(ls):
    return isinstance(ls, cons) and (ls.cdr is symbol_emptylist)

def length_two_q(ls):
    return (isinstance(ls, cons) and 
            isinstance(ls.cdr, cons) and 
            (ls.cdr.cdr is symbol_emptylist))

def length_at_least_q(n, ls):
    length = len(list(ls))
    return length >= n

def all_numeric_q(ls):
    for item in ls:
        if not number_q(item):
            return False
    return True

def list_native(iterable):
    return list(iterable)

### Questions:

def even_q(n):
    return n % 2 == 0

def odd_q(n):
    return n % 2 == 1

def eq_q(o1, o2):
    return o1 is o2

def char_q(item):
    return isinstance(item, Char)

def string_q(item):
    if PY3:
        return isinstance(item, str)
    else:
        return isinstance(item, (str, unicode))

def char_whitespace_q(c):
    return c.char in [' ', '\t', '\n', '\r']

def char_alphabetic_q(c):
    return (('A' <= c.char <= 'Z') or 
            ('a' <= c.char <= 'z'))

def char_numeric_q(c):
    return '0' <= c.char <= '9'

def char_is__q(c1, c2):
    return c1 == c2

def number_q(item):
    return isinstance(item, (int, float, fractions.Fraction))

def null_q(item):
    return item is symbol_emptylist

def boolean_q(item):
    return isinstance(item, bool)

def true_q(item):
    if item is False:
        return False
    else:
        return True

def list_q(item):
    ## return proper_list?
    current = item
    while isinstance(current, cons):
        current = current.cdr
    return current is symbol_emptylist

def procedure_q(item):
    return pair_q(item) and (car(item) is symbol_procedure)

def symbol_q(item):
    return isinstance(item, Symbol)

def vector_q(item):
    return isinstance(item, list)

def pair_q(item):
    return isinstance(item, cons)

def iterator_q(item):
    # return true if an iter that implementation doesn't
    # know how to handle. Python knows how to handle all
    # of the iters, but IronPython can import other
    # things.
    return hasattr(item, "MoveNext")

def get_iterator(generator):
    # Not used in Python version
    return iter(generator)

def get_type(obj):
    return type(obj)

### Math and applications:

def fraction_repr(self):
    if self.denominator == 1:
        return str(self.numerator)
    return "%s/%s" % (self.numerator, self.denominator)

fractions.Fraction.__repr__ = fraction_repr 
fractions.Fraction.__str__ = fraction_repr

def modulo(a, b):
    return a % b

def quotient(a, b):
    return int(a / b)

def remainder(a, b):
    return a % b

def sqrt(number):
    return math.sqrt(number)

def plus(*args):
    return functools.reduce(operator.add, args, 0)

def minus(*args):
    if len(args) == 0:
        return 0
    elif len(args) == 1:
        return -args[0]
    else:
        return functools.reduce(operator.sub, args[1:], args[0])

def multiply(*args):
    return functools.reduce(operator.mul, args, 1)

def divide(*args):
    try:
        if len(args) == 0:
            return 1
        elif len(args) == 1:
            return fractions.Fraction(1, args[0])
        else:
            current = fractions.Fraction(args[0], args[1])
            for arg in args[2:]:
                current = fractions.Fraction(current, arg)
            return current
    except:
        return functools.reduce(operator.truediv, args)

def Equal(o1, o2):
    if boolean_q(o1) or boolean_q(o2):
        return boolean_q(o1) and boolean_q(o2) and o1 is o2
    return o1 == o2

def equal_q(o1, o2):
    if boolean_q(o1) or boolean_q(o2):
        return boolean_q(o1) and boolean_q(o2) and o1 is o2
    return o1 == o2

def LessThan(a, b):
    return a < b

def LessThanEqual(a, b):
    return a <= b

def GreaterThanEqual(a, b):
    return a >= b

def GreaterThan(a, b):
    return a > b

def memq(item, lyst):
    current = lyst
    while isinstance(current, cons):
        if current.car is item:
            return current
        current = current.cdr
    return False

### Converters:

def char_to_integer(c):
    return ord(c.char)

def integer_to_char(i):
    return make_char(chr(i))

def number_to_string(number):
    return str(number)

def string_to_integer(s):
    return int(s)

def string_to_symbol(string):
    return make_symbol(string)

def list_to_string(lyst):
    # only on list of chars
    retval = ""
    current = lyst
    while isinstance(current, cons):
        retval += current.car.char
        current = current.cdr
    return retval

def list_to_vector(lyst):
    # this works because cons implements iter
    return Vector(lyst)

def vector_to_list(vector):
    return List(*vector)

def vector_ref(vector, position):
    return vector[position]

def char_to_string(c):
    return c.char

def string_to_list(st):
    return List(*[make_char(c) for c in st])

def symbol_to_string(symbol):
    return symbol.name

def string_to_decimal(s):
    return float(s)

def string_to_rational(s):
    try:
        return fractions.Fraction(s)
    except:
        return False

def string_to_number(s):
    if "/" in s:
        return string_to_rational(s)
    elif "." in s:
        return string_to_decimal(s)
    else:
        return string_to_integer(s)

def int_(number):
    return int(round(number))

### Strings:

def string_append(*args):
    return "".join([str(arg) for arg in args])

def string_ref(string, pos):
    return make_char(string[pos])

def string(*chars):
    retval = ""
    for c in chars:
        if isinstance(c, Char):
            retval += c.char
        else:
            raise Exception("invalid argument to string: '%s' is not a character" % c)
    return retval

def string_split(string, delim):
    return List(*string.split(delim.char))

def member(item, lyst):
    current = lyst
    while isinstance(current, cons):
        if item == current.car:
            return True
        current = current.cdr
    return False

def string_is__q(s1, s2):
    return s1 == s2

def string_length(s):
    return len(s)

def stringLessThan_q(s1, s2):
    return s1 < s2

def substring(s, start, stop):
    return s[start:stop]

### Functions:

def Apply(f, lyst):
    return f(*list_to_vector(lyst))

### Annotated expression support:

def tagged_list_hat(keyword, op, length):
    def tagged_list(asexp):
        return (list_q_hat(asexp) and
                op(length_hat(asexp), length) and
                symbol_q_hat(car_hat(asexp)) and 
                eq_q_hat(car_hat(asexp), keyword))
    return tagged_list

def tagged2_list_hat(keyword, op, length):
    def tagged2_list(asexp):
        return (list_q_hat(asexp) and
                op(length_hat(asexp), length) and
                symbol_q_hat(car_hat(asexp)) and 
                eq_q_hat(cadr_hat(asexp), keyword))
    return tagged2_list

### Misc:

def error(function, message):
    raise Exception("Exception in %s: %s" % (function, message))

def display(item):
    print(item, end="")

def printf(formatting, *items):
    print(format(formatting, *items), end="")

def newline():
    print()

def trampoline():
    global pc, exception_reg
    if ENVIRONMENT.get("DEBUG", False) == True:
        while pc:
            pc()
    else:
        while pc:
            try:
                pc()
            except DebugException:
                raise
            except KeyboardInterrupt:
                exception_reg = make_exception("KeyboardInterrupt", "Keyboard interrupt", symbol_none, symbol_none, symbol_none)
                pc = apply_handler2            
            except Exception as e:
                #arginfo = inspect.getargvalues(sys.exc_info()[2].tb_frame)
                #extra = "\nArguments:\n"
                #for arg in arginfo.args:
                #    extra += "   %s = %s\n" % (arg, repr(arginfo.locals[arg]))
                #extra += "\nLocals:\n"
                #for arg in arginfo.locals:
                #    extra += "   %s = %s\n" % (arg, repr(arginfo.locals[arg]))
                exception_reg = make_exception("UnhandledException", str(e), symbol_none, symbol_none, symbol_none)
                pc = apply_handler2
    return final_reg

def box(item):
    return List(item)

def ready_to_eval(text):
    if text:
        lines = text.split("\n")
        if len(lines) > 0 and lines[-1].strip() == "":
            return True ## force it
        ## else, only if valid parse
        return try_parse(text)
    return True

# native:
def read_multiline(prompt):
    retval = ""
    while True:
        try:
            if retval:
                retval += "\n"
            if PY3:
                retval += input(prompt) ## Python 3
            else:
                retval += raw_input(prompt) ## Python 2
            prompt = "... "
        except EOFError:
            return "(exit)"
        except:
            return ""
        if ready_to_eval(retval):
            return retval
        retval += " "

def format(formatting, *lyst):
    args = list_to_vector(lyst)
    retval = ""
    i = 0
    count = 0
    while i < len(formatting):
        if formatting[i] == '\\':
            i += 1
        elif formatting[i] == "~":
            if formatting[i+1] == 's' and count < len(args):
                i += 1
                retval += make_safe(args[count])
                count += 1
            elif formatting[i+1] == 'a' and count < len(args):
                i += 1
                retval += str(args[count])
                count += 1
            elif formatting[i+1] == '%':
                i += 1
                retval += "\n"
            else:
                retval += formatting[i] # unknown ~X
        else:
            retval += formatting[i]
        i += 1
    return retval

def pretty_print(thing):
    print(thing)

def make_safe(item):
    if procedure_q(item):
        return "#<procedure>"
    elif environment_q(item):
        return "#<environment>"
    elif string_q(item):
        # Unlike Python, Scheme's strings must start with "
        return '"%s"' % item.replace('"', '\\"')
    elif boolean_q(item):
        return "#t" if item else "#f"
    else:
        return repr(item)

def search_frame(frame, variable):
    if isinstance(frame, cons):
        bindings = car(frame)
        variables = cadr(frame)
        i = 0
        while not null_q(variables):
            if eq_q(car(variables), variable):
                return bindings[i]
            variables = cdr(variables)
            i += 1
        return False
    else:
        raise Exception("invalid frame")

def read_content(filename):
    return open(filename).read()

def file_exists_q(path):
    return os.path.isfile(path)

def get_current_time():
    return time.time()

def current_directory(*path):
    if len(path) == 1:
        os.chdir(path[0])
    return os.getcwd()

def Range(*args):
    return List(*range(*args))

def assv(x, ls):
    while isinstance(ls, cons):
        if x is caar(ls):
            return ls.car
        ls = ls.cdr
    return False

def memv(item, ls):
    current = ls
    while isinstance(current, cons):
        if (item == current.car):
            return current
        current = current.cdr
    return False

def make_vector(size):
    return Vector([0] * size)

class Vector(list):
    def __repr__(self):
        return "#%d(%s)" % (len(self), " ".join(map(repr, self)))

def vector_native(*ls):
    return Vector(ls)

def vector_set_b(vec, pos, value):
    vec[pos] = value

def eqv_q(a, b):
    if number_q(a) and number_q(b):
        # but be same type, and value
        return type(a) == type(b) and eq_q(a, b)
    elif char_q(a) and char_q(b):
        return a.char == b.char
    else:
        return eq_q(a, b)

def atom_q(item):
    return number_q(item) or symbol_q(item) or string_q(item)

def iter_q(item):
    return isinstance(item, Iterable)

def assq(x, ls):
    while not null_q(ls):
        if eq_q(x, caar(ls)):
            return car(ls)
        ls = cdr(ls)
    return False

### External env interface:

def import_native(libraries, environment):
    env = {}
    for library in libraries:
        if PY3:
            exec("import %s" % library, env)
        else:
            exec ("import %s" % library) in env
    ENVIRONMENT.update(env)
    return List(*[make_symbol(name) for name in env.keys() if not name.startswith("_")])

def import_as_native(library, name, environment):
    env = {}
    if name == make_symbol("*") or name == "*":
        if PY3:
            exec("from %s import *" % library, env)
        else:
            exec ("from %s import *" % library) in env
    else:
        if PY3:
            exec("import %s as %s" % (library, name), env)
        else:
            exec ("import %s as %s" % (library, name)) in env
    ENVIRONMENT.update(env)
    return List(*[make_symbol(name) for name in env.keys() if not name.startswith("_")])

def import_from_native(library, name_list, environment):
    env = {}
    if PY3:
        exec("from %s import %s" % (library, ", ".join([str(name) for name in name_list])), env)
    else:
        exec ("from %s import %s" % (library, ", ".join([str(name) for name in name_list]))) in env
    ENVIRONMENT.update(env)
    return List(*[make_symbol(name) for name in env.keys() if not name.startswith("_")])

def dlr_proc_q(item):
    return (callable(item) and not isinstance(item, cons)) or hasattr(item, "MoveNext")

def dlr_env_contains(item):
    return item.name in ENVIRONMENT

def set_global_value_b(variable, value):
    ENVIRONMENT[variable.name] = value

def dlr_env_lookup(variable):
    return ENVIRONMENT[variable.name]

def dlr_object_contains(obj, components):
    # components: (math sqrt)
    retval = obj
    for component in cdr(components):
        if hasattr(retval, component.name):
            retval = getattr(retval, component.name)
        else:
            return False
    return True

def get_external_member(obj, components):
    # components: (math sqrt)
    retval = obj
    for component in cdr(components):
        if hasattr(retval, component.name):
            retval = getattr(retval, component.name)
        else:
            return void_value
    return retval

def dlr_apply(f, args):
    ## FIXME: Handle named params, and (* : ...), (** : ...)
    largs = list_to_vector(args)
    return f(*largs)

def dlr_func(schemeProc):
    def f(*args):
        GLOBALS["proc_reg"] = schemeProc
        GLOBALS["args_reg"] = List(*args)
        GLOBALS["handler_reg"] = REP_handler
        GLOBALS["k2_reg"] = REP_k
        GLOBALS["pc"] = apply_proc
        return trampoline()
    return f

def set_global_docstring_b(variable, docstring):
    pass

def get_external_members(obj):
    return List(*[make_symbol(x) for x in  dir(obj)])

def callback(schemeProc):
    def cb(*args):
        GLOBALS["proc_reg"] = schemeProc
        GLOBALS["args_reg"] = List(*args)
        GLOBALS["handler_reg"] = REP_handler
        GLOBALS["k2_reg"] = REP_k
        GLOBALS["pc"] = apply_proc
        return trampoline()
    return cb

def set_external_member_b(obj, components, value):
    for component in components[1:-1]:
        obj = getattr(obj, component.name)
    setattr(obj, components[-1].name, value)

def apply_star(external_function, args):
    return external_function(*args)

def next_item(iter_item):
    try:
        return next(iter_item)
    except StopIteration:
        return symbol_emptylist

def load_native(filename):
    GLOBALS["handler_reg"] = REP_handler
    GLOBALS["k2_reg"] = REP_k
    GLOBALS['env2_reg'] = toplevel_env
    GLOBALS['filenames_reg'] = List(filename)
    GLOBALS['pc'] = load_files
    trampoline()

def getitem_native(dictionary, item):
    return dictionary[item]

def setitem_native(dictionary, item, value):
    dictionary[item] = value
    return value

def contains_native(dictionary, item):
    return item in dictionary

def highlight_expression(exp):
    info = symbol_undefined
    info = rac(exp)
    if true_q(not((info) is (symbol_none))):
        if GLOBALS.get("TRACE_GUI", False):
            GLOBALS["TRACE_GUI_COUNT"] += 1
            if GLOBALS["TRACE_GUI_COUNT"] % 2 == 1:
                raise DebugException([get_start_line(info), get_start_char(info), get_end_line(info), get_end_char(info)])
        else:
            printf("call: ~s~%", aunparse(exp))

# end of Scheme.py
#############################################################

symbol_emptylist = make_symbol("()")
symbol_continuation = make_symbol("continuation")
symbol_none = make_symbol("none")
symbol_quasiquote = make_symbol("quasiquote")
symbol_else = make_symbol("else")
symbol_, = make_symbol(",")
symbol_,name = make_symbol(",name")
symbol_unit = make_symbol("unit")
symbol_composite = make_symbol("composite")
symbol_continuation2 = make_symbol("continuation2")
symbol_undefined = make_symbol("undefined")
symbol_,value1 = make_symbol(",value1")
symbol_cases = make_symbol("cases")
symbol_,type_name = make_symbol(",type-name")
symbol_stdin = make_symbol("stdin")
symbol_end_marker = make_symbol("end-marker")
symbol_continuation3 = make_symbol("continuation3")
symbol_continuation4 = make_symbol("continuation4")
symbol_dot = make_symbol("dot")
symbol_fail_continuation = make_symbol("fail-continuation")
symbol_handler = make_symbol("handler")
symbol_exception = make_symbol("exception")
symbol_handler2 = make_symbol("handler2")
symbol_procedure = make_symbol("procedure")
symbol_ok = make_symbol("ok")
symbol_macro_transformer = make_symbol("macro-transformer")
symbol_True = make_symbol("#t")
symbol_False = make_symbol("#f")
symbol__is_to_ = make_symbol("=>")
symbol_r = make_symbol("r")
symbol_token_start_state = make_symbol("token-start-state")
symbol_error = make_symbol("error")
symbol_apply_action = make_symbol("apply-action")
symbol_integer = make_symbol("integer")
symbol_decimal = make_symbol("decimal")
symbol_rational = make_symbol("rational")
symbol_identifier = make_symbol("identifier")
symbol_boolean = make_symbol("boolean")
symbol_character = make_symbol("character")
symbol_string = make_symbol("string")
symbol_apply_state = make_symbol("apply-state")
symbol_quote = make_symbol("quote")
symbol_unquote = make_symbol("unquote")
symbol_unquote_splicing = make_symbol("unquote-splicing")
symbol_rparen = make_symbol("rparen")
symbol_rbracket = make_symbol("rbracket")
symbol_environment = make_symbol("environment")
symbol_args = make_symbol("args")
symbol_and = make_symbol("and")
symbol_or = make_symbol("or")
symbol_cond = make_symbol("cond")
symbol_let = make_symbol("let")
symbol_letrec = make_symbol("letrec")
symbol_let_star = make_symbol("let*")
symbol_case = make_symbol("case")
symbol_record_case = make_symbol("record-case")
symbol_define_datatype = make_symbol("define-datatype")
symbol_pattern_macro = make_symbol("pattern-macro")
symbol_,ax = make_symbol(",ax")
symbol_,datum = make_symbol(",datum")
symbol_aunparse = make_symbol("aunparse")
symbol_goodbye = make_symbol("goodbye")
symbol_m = make_symbol("m")
symbol_application = make_symbol("application")
symbol_unknown = make_symbol("unknown")
symbol_macro_generated_exp = make_symbol("macro-generated-exp")
symbol_colon = make_symbol(":")
symbol_b_procedure_d = make_symbol("<procedure>")
symbol_b_environment_d = make_symbol("<environment>")
symbol_Map = make_symbol("map")
symbol_multiply = make_symbol("*")
symbol_plus = make_symbol("+")
symbol_minus = make_symbol("-")
symbol_divide = make_symbol("/")
symbol_div = make_symbol("div")
symbol_p = make_symbol("%")
symbol_mod = make_symbol("mod")
symbol_modulo = make_symbol("modulo")
symbol___ = make_symbol("//")
symbol_quotient = make_symbol("quotient")
symbol_LessThan = make_symbol("<")
symbol_LessThanEqual = make_symbol("<=")
symbol_Equal = make_symbol("=")
symbol_GreaterThan = make_symbol(">")
symbol_GreaterThanEqual = make_symbol(">=")
symbol_abort = make_symbol("abort")
symbol_abs = make_symbol("abs")
symbol_append = make_symbol("append")
symbol_Apply = make_symbol("apply")
symbol_assv = make_symbol("assv")
symbol_boolean_q = make_symbol("boolean?")
symbol_caddr = make_symbol("caddr")
symbol_cadr = make_symbol("cadr")
symbol_call_with_current_continuation = make_symbol("call-with-current-continuation")
symbol_call_cc = make_symbol("call/cc")
symbol_car = make_symbol("car")
symbol_cdr = make_symbol("cdr")
symbol_caaaar = make_symbol("caaaar")
symbol_caaadr = make_symbol("caaadr")
symbol_caaar = make_symbol("caaar")
symbol_caadar = make_symbol("caadar")
symbol_caaddr = make_symbol("caaddr")
symbol_caadr = make_symbol("caadr")
symbol_caar = make_symbol("caar")
symbol_cadaar = make_symbol("cadaar")
symbol_cadadr = make_symbol("cadadr")
symbol_cadar = make_symbol("cadar")
symbol_caddar = make_symbol("caddar")
symbol_cadddr = make_symbol("cadddr")
symbol_cdaaar = make_symbol("cdaaar")
symbol_cdaadr = make_symbol("cdaadr")
symbol_cdaar = make_symbol("cdaar")
symbol_cdadar = make_symbol("cdadar")
symbol_cdaddr = make_symbol("cdaddr")
symbol_cdadr = make_symbol("cdadr")
symbol_cdar = make_symbol("cdar")
symbol_cddaar = make_symbol("cddaar")
symbol_cddadr = make_symbol("cddadr")
symbol_cddar = make_symbol("cddar")
symbol_cdddar = make_symbol("cdddar")
symbol_cddddr = make_symbol("cddddr")
symbol_cdddr = make_symbol("cdddr")
symbol_cddr = make_symbol("cddr")
symbol_char_q = make_symbol("char?")
symbol_char_is__q = make_symbol("char=?")
symbol_char_whitespace_q = make_symbol("char-whitespace?")
symbol_char_alphabetic_q = make_symbol("char-alphabetic?")
symbol_char_numeric_q = make_symbol("char-numeric?")
symbol_char_to_integer = make_symbol("char->integer")
symbol_cons = make_symbol("cons")
symbol_current_time = make_symbol("current-time")
symbol_cut = make_symbol("cut")
symbol_dir = make_symbol("dir")
symbol_display = make_symbol("display")
symbol_current_environment = make_symbol("current-environment")
symbol_eq_q = make_symbol("eq?")
symbol_equal_q = make_symbol("equal?")
symbol_eval = make_symbol("eval")
symbol_eval_ast = make_symbol("eval-ast")
symbol_exit = make_symbol("exit")
symbol_for_each = make_symbol("for-each")
symbol_format = make_symbol("format")
symbol_get = make_symbol("get")
symbol_get_stack_trace = make_symbol("get-stack-trace")
symbol_load_as = make_symbol("load-as")
symbol_integer_to_char = make_symbol("integer->char")
symbol_length = make_symbol("length")
symbol_List = make_symbol("list")
symbol_list_to_vector = make_symbol("list->vector")
symbol_list_to_string = make_symbol("list->string")
symbol_list_ref = make_symbol("list-ref")
symbol_load = make_symbol("load")
symbol_min = make_symbol("min")
symbol_max = make_symbol("max")
symbol_make_set = make_symbol("make-set")
symbol_make_vector = make_symbol("make-vector")
symbol_member = make_symbol("member")
symbol_memq = make_symbol("memq")
symbol_memv = make_symbol("memv")
symbol_newline = make_symbol("newline")
symbol_not = make_symbol("not")
symbol_null_q = make_symbol("null?")
symbol_number_to_string = make_symbol("number->string")
symbol_number_q = make_symbol("number?")
symbol_pair_q = make_symbol("pair?")
symbol_parse = make_symbol("parse")
symbol_parse_string = make_symbol("parse-string")
symbol_print = make_symbol("print")
symbol_printf = make_symbol("printf")
symbol_Range = make_symbol("range")
symbol_read_string = make_symbol("read-string")
symbol_require = make_symbol("require")
symbol_reverse = make_symbol("reverse")
symbol_set_car_b = make_symbol("set-car!")
symbol_set_cdr_b = make_symbol("set-cdr!")
symbol_snoc = make_symbol("snoc")
symbol_rac = make_symbol("rac")
symbol_rdc = make_symbol("rdc")
symbol_sqrt = make_symbol("sqrt")
symbol_odd_q = make_symbol("odd?")
symbol_even_q = make_symbol("even?")
symbol_remainder = make_symbol("remainder")
symbol_string_length = make_symbol("string-length")
symbol_string_ref = make_symbol("string-ref")
symbol_string_q = make_symbol("string?")
symbol_string_to_number = make_symbol("string->number")
symbol_string_is__q = make_symbol("string=?")
symbol_substring = make_symbol("substring")
symbol_symbol_q = make_symbol("symbol?")
symbol_unparse = make_symbol("unparse")
symbol_unparse_procedure = make_symbol("unparse-procedure")
symbol_import = make_symbol("import")
symbol_import_as = make_symbol("import-as")
symbol_import_from = make_symbol("import-from")
symbol_use_stack_trace = make_symbol("use-stack-trace")
symbol_vector = make_symbol("vector")
symbol_vector_ref = make_symbol("vector-ref")
symbol_vector_set_b = make_symbol("vector-set!")
symbol_void = make_symbol("void")
symbol_zero_q = make_symbol("zero?")
symbol_current_directory = make_symbol("current-directory")
symbol_cd = make_symbol("cd")
symbol_round = make_symbol("round")
symbol_char_to_string = make_symbol("char->string")
symbol_string_to_list = make_symbol("string->list")
symbol_string_to_symbol = make_symbol("string->symbol")
symbol_symbol_to_string = make_symbol("symbol->string")
symbol_vector_to_list = make_symbol("vector->list")
symbol_eqv_q = make_symbol("eqv?")
symbol_vector_q = make_symbol("vector?")
symbol_atom_q = make_symbol("atom?")
symbol_iter_q = make_symbol("iter?")
symbol_list_q = make_symbol("list?")
symbol_procedure_q = make_symbol("procedure?")
symbol_stringLessThan_q = make_symbol("string<?")
symbol_float = make_symbol("float")
symbol_globals = make_symbol("globals")
symbol_int_ = make_symbol("int")
symbol_assq = make_symbol("assq")
symbol_dict = make_symbol("dict")
symbol_contains = make_symbol("contains")
symbol_getitem = make_symbol("getitem")
symbol_setitem = make_symbol("setitem")
symbol_property = make_symbol("property")
symbol_reset_toplevel_env = make_symbol("reset-toplevel-env")
symbol_sort = make_symbol("sort")
symbol_string_append = make_symbol("string-append")
symbol_string_split = make_symbol("string-split")
symbol_symbol = make_symbol("symbol")
symbol_typeof = make_symbol("typeof")
symbol_use_lexical_address = make_symbol("use-lexical-address")
symbol_use_tracing = make_symbol("use-tracing")
symbol_process_params_by_pos = make_symbol("process-params-by-pos")
symbol_clean_up_params = make_symbol("clean-up-params")
symbol__star_star = make_symbol("**")
symbol__ = make_symbol("_")
symbol_empty = make_symbol("empty")
symbol_instantiate_hat = make_symbol("instantiate^")
symbol_substitution = make_symbol("substitution")
symbol_apply_sub_hat = make_symbol("apply-sub^")
symbol_atom = make_symbol("atom")
symbol_pair = make_symbol("pair")
symbol_if = make_symbol("if")
symbol_help = make_symbol("help")
symbol_set_b = make_symbol("set!")
symbol_func = make_symbol("func")
symbol_callback = make_symbol("callback")
symbol_define = make_symbol("define")
symbol_define_b = make_symbol("define!")
symbol_define_syntax = make_symbol("define-syntax")
symbol_begin = make_symbol("begin")
symbol_lambda = make_symbol("lambda")
symbol_trace_lambda = make_symbol("trace-lambda")
symbol_raise = make_symbol("raise")
symbol_choose = make_symbol("choose")
symbol_try = make_symbol("try")
symbol_catch = make_symbol("catch")
symbol_finally = make_symbol("finally")
symbol_b__q_q_q_d = make_symbol("<???>")
symbol_b_fail_d = make_symbol("<fail>")
symbol_b_handler_d = make_symbol("<handler>")
symbol_b_void_d = make_symbol("<void>")

define_datatype(aexpression, aexpression_q, lit_aexp(datum(anything_q), info(source_info_q)), var_aexp(id(symbol_q), info(source_info_q)), lexical_address_aexp(depth(number_q), offset(number_q), id(symbol_q), info(source_info_q)), if_aexp(test_aexp(aexpression_q), then_aexp(aexpression_q), else_aexp(aexpression_q), info(source_info_q)), help_aexp(var(symbol_q), var_info(source_info_q), info(source_info_q)), association_aexp(var(symbol_q), exp(aexpression_q), info(source_info_q)), assign_aexp(var(symbol_q), rhs_exp(aexpression_q), var_info(source_info_q), info(source_info_q)), func_aexp(exp(aexpression_q), info(source_info_q)), callback_aexp(exp(aexpression_q), info(source_info_q)), define_aexp(id(symbol_q), docstring(string_q), rhs_exp(aexpression_q), info(source_info_q)), define_b_aexp(id(symbol_q), docstring(string_q), rhs_exp(aexpression_q), info(source_info_q)), define_syntax_aexp(name(symbol_q), clauses(list_of(define_syntax_clause_q)), aclauses(list_of_define_syntax_clauses_q_hat), info(source_info_q)), begin_aexp(exps(list_of(aexpression_q)), info(source_info_q)), lambda_aexp(formals(list_of(lambda(e(), (symbol_q(e)) or (association_q(e))))), bodies(list_of(aexpression_q)), info(source_info_q)), mu_lambda_aexp(formals(list_of(lambda(e(), (symbol_q(e)) or (association_q(e))))), runt(lambda(e(), (symbol_q(e)) or (association_q(e)))), bodies(list_of(aexpression_q)), info(source_info_q)), trace_lambda_aexp(name(symbol_q), formals(list_of(lambda(e(), (symbol_q(e)) or (association_q(e))))), bodies(list_of(aexpression_q)), info(source_info_q)), mu_trace_lambda_aexp(name(symbol_q), formals(list_of(lambda(e(), (symbol_q(e)) or (association_q(e))))), runt(lambda(e(), (symbol_q(e)) or (association_q(e)))), bodies(list_of(aexpression_q)), info(source_info_q)), app_aexp(operator(aexpression_q), operands(list_of(aexpression_q)), info(source_info_q)), try_catch_aexp(body(aexpression_q), catch_var(symbol_q), catch_exps(list_of(aexpression_q)), info(source_info_q)), try_finally_aexp(body(aexpression_q), finally_exps(list_of(aexpression_q)), info(source_info_q)), try_catch_finally_aexp(body(aexpression_q), catch_var(symbol_q), catch_exps(list_of(aexpression_q)), finally_exps(list_of(aexpression_q)), info(source_info_q)), raise_aexp(exp(aexpression_q), info(source_info_q)), choose_aexp(exps(list_of(aexpression_q)), info(source_info_q)))
def apply_cont(k, value):
    applyplus(cadr(k), value, cddr(k))

def b_cont_1_d(value, fields):
    chars = car(fields)
    fail = cadr(fields)
    k = caddr(fields)
    apply_cont3(k, value, chars, fail)

def b_cont_2_d(value, fields):
    v1 = car(fields)
    info = cadr(fields)
    k = caddr(fields)
    apply_cont(k, List(pair_tag, v1, value, info))

def b_cont_3_d(value, fields):
    x = car(fields)
    info = cadr(fields)
    k = caddr(fields)
    annotate_cps(cdr(x), symbol_none, make_cont(b_cont_2_d, value, info, k))

def b_cont_4_d(value, fields):
    k = car(fields)
    apply_cont(k, list_to_vector(value))

def b_cont_5_d(value, fields):
    v1 = car(fields)
    k = cadr(fields)
    apply_cont(k, cons(v1, value))

def b_cont_6_d(value, fields):
    x = car(fields)
    k = cadr(fields)
    unannotate_cps(cdr(x), make_cont(b_cont_5_d, value, k))

def b_cont_7_d(value, fields):
    x = car(fields)
    k = cadr(fields)
    unannotate_cps(caddr(x), make_cont(b_cont_5_d, value, k))

def b_cont_8_d(value, fields):
    end = car(fields)
    tokens_left = cadr(fields)
    fail = caddr(fields)
    k = cadddr(fields)
    apply_cont4(k, value, end, tokens_left, fail)

def b_cont_9_d(value, fields):
    end = car(fields)
    tokens = cadr(fields)
    fail = caddr(fields)
    k = cadddr(fields)
    apply_cont4(k, value, end, rest_of(tokens), fail)

def b_cont_10_d(value, fields):
    src = car(fields)
    start = cadr(fields)
    tokens = caddr(fields)
    handler = cadddr(fields)
    fail = list_ref(fields, 4)
    k = list_ref(fields, 5)
    read_sexp(rest_of(tokens), src, handler, fail, make_cont4(b_cont4_3_d, src, start, value, k))

def b_cont_11_d(value, fields):
    halt_star(value)

def b_cont_12_d(value, fields):
    adatum = car(fields)
    senv = cadr(fields)
    info = caddr(fields)
    handler = cadddr(fields)
    fail = list_ref(fields, 4)
    k = list_ref(fields, 5)
    formals_list = (value if list_q(value) else cons(last(value), head(value)))
    name = untag_atom_hat(cadr_hat(adatum))
    aparse_all(cdddr_hat(adatum), cons(formals_list, senv), handler, fail, make_cont2(b_cont2_16_d, name, value, info, k))

def b_cont_13_d(value, fields):
    adatum = car(fields)
    senv = cadr(fields)
    info = caddr(fields)
    handler = cadddr(fields)
    fail = list_ref(fields, 4)
    k = list_ref(fields, 5)
    formals_list = (value if list_q(value) else cons(last(value), head(value)))
    aparse_all(cddr_hat(adatum), cons(formals_list, senv), handler, fail, make_cont2(b_cont2_17_d, value, info, k))

def b_cont_14_d(value, fields):
    aclauses = car(fields)
    name = cadr(fields)
    info = caddr(fields)
    fail = cadddr(fields)
    k = list_ref(fields, 4)
    apply_cont2(k, define_syntax_aexp(name, value, aclauses, info), fail)

def b_cont_15_d(value, fields):
    senv = car(fields)
    info = cadr(fields)
    handler = caddr(fields)
    fail = cadddr(fields)
    k = list_ref(fields, 4)
    aparse(replace_info(value, info), senv, handler, fail, k)

def b_cont_16_d(value, fields):
    senv = car(fields)
    info = cadr(fields)
    handler = caddr(fields)
    fail = cadddr(fields)
    k = list_ref(fields, 4)
    annotate_cps(value, symbol_none, make_cont(b_cont_15_d, senv, info, handler, fail, k))

def b_cont_17_d(value, fields):
    adatum = car(fields)
    senv = cadr(fields)
    info = caddr(fields)
    handler = cadddr(fields)
    fail = list_ref(fields, 4)
    k = list_ref(fields, 5)
    if true_q(original_source_info_q(adatum)):
        aparse(replace_info(value, snoc(symbol_quasiquote, info)), senv, handler, fail, k)
    else:
        aparse(replace_info(value, info), senv, handler, fail, k)

def b_cont_18_d(value, fields):
    adatum = car(fields)
    senv = cadr(fields)
    info = caddr(fields)
    handler = cadddr(fields)
    fail = list_ref(fields, 4)
    k = list_ref(fields, 5)
    annotate_cps(value, symbol_none, make_cont(b_cont_17_d, adatum, senv, info, handler, fail, k))

def b_cont_19_d(value, fields):
    info = car(fields)
    fail = cadr(fields)
    k = caddr(fields)
    apply_cont2(k, lit_aexp(cadr(value), info), fail)

def b_cont_20_d(value, fields):
    info = car(fields)
    fail = cadr(fields)
    k = caddr(fields)
    apply_cont2(k, lit_aexp(value, info), fail)

def b_cont_21_d(value, fields):
    msg = car(fields)
    info = cadr(fields)
    handler = caddr(fields)
    fail = cadddr(fields)
    apply_handler2(handler, make_exception("ParseError", format("~s ~a", msg, value), get_srcfile(info), get_start_line(info), get_start_char(info)), fail)

def b_cont_22_d(value, fields):
    bindings = car(fields)
    k = cadr(fields)
