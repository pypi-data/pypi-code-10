#!/usr/bin/env python

#-----------------------------------------------------------------------------------------------------------------------
# INFO:
#-----------------------------------------------------------------------------------------------------------------------

"""
Author: Evan Hubinger
License: Apache 2.0
Description: The Coconut transpiler.
"""

#-----------------------------------------------------------------------------------------------------------------------
# IMPORTS:
#-----------------------------------------------------------------------------------------------------------------------

from __future__ import with_statement, print_function, absolute_import, unicode_literals, division

from .root import *
from pyparsing import *

#-----------------------------------------------------------------------------------------------------------------------
# HEADERS:
#-----------------------------------------------------------------------------------------------------------------------

def headers(which, version=None):
    if which == "none":
        return ""
    if which == "initial" or which == "package":
        if version is None:
            header = "#!/usr/bin/env python"
        elif version == "2":
            header = "#!/usr/bin/env python2"
        elif version == "3":
            header = "#!/usr/bin/env python3"
        else:
            raise CoconutException("invalid Python version: "+repr(version))
        header += '''
# -*- coding: '''+ENCODING+''' -*-

# Compiled with Coconut version '''+VERSION_STR+'''

'''
        if which == "package":
            header += '''"""Built-in Coconut functions."""

'''
    else:
        header = ""
    if which != "initial":
        header = r'''# Coconut Header: --------------------------------------------------------------
'''
        if which == "code":
            if version != "3":
                header += r'''
from __future__ import with_statement, print_function, absolute_import, unicode_literals, division
'''
        elif version is None:
            header += r'''
from __future__ import with_statement, print_function, absolute_import, unicode_literals, division
import sys as _coconut_sys
if _coconut_sys.version_info < (3,):
    py2_filter, py2_hex, py2_map, py2_oct, py2_zip = filter, hex, map, oct, zip
    from future_builtins import *
    py2_range, range = range, xrange
    py2_int = int
    _coconut_int, _coconut_long = int, long
    class _coconut_metaint(type):
        def __instancecheck__(cls, inst):
            return isinstance(inst, (_coconut_int, _coconut_long))
    class int(_coconut_int):
        """Python 3 int."""
        __metaclass__ = _coconut_metaint
    py2_chr, chr = chr, unichr
    bytes, str = str, unicode
    _coconut_encoding = "'''+ENCODING+r'''"
    py2_print = print
    _coconut_print = print
    def print(*args, **kwargs):
        """Python 3 print."""
        return _coconut_print(*(str(x).encode(_coconut_encoding) for x in args), **kwargs)
    py2_input = raw_input
    _coconut_input = raw_input
    def input(*args, **kwargs):
        """Python 3 input."""
        return _coconut_input(*args, **kwargs).decode(_coconut_encoding)
'''
        elif version == "2":
            header += r'''
from __future__ import with_statement, print_function, absolute_import, unicode_literals, division
py2_filter, py2_hex, py2_map, py2_oct, py2_zip = filter, hex, map, oct, zip
from future_builtins import *
py2_range, range = range, xrange
py2_int = int
_coconut_int, _coconut_long = int, long
class _coconut_metaint(type):
    def __instancecheck__(cls, inst):
        return isinstance(inst, (_coconut_int, _coconut_long))
class int(_coconut_int):
    """Python 3 int."""
    __metaclass__ = _coconut_metaint
py2_chr, chr = chr, unichr
bytes, str = str, unicode
_coconut_encoding = "'''+ENCODING+r'''"
py2_print = print
_coconut_print = print
def print(*args, **kwargs):
    """Python 3 print."""
    return _coconut_print(*(str(x).encode(_coconut_encoding) for x in args), **kwargs)
py2_input = raw_input
_coconut_input = raw_input
def input(*args, **kwargs):
    """Python 3 input."""
    return _coconut_input(*args, **kwargs).decode(_coconut_encoding)
'''
        if which == "package":
            header += r'''
version = "'''+VERSION+r'''"

import functools
import operator
import itertools
import collections
'''
            if version == "2":
                header += r'''abc = collections
'''
            elif version == "3":
                header += r'''import collections.abc as abc
'''
            else:
                header += r'''try:
    import collections.abc as abc
except ImportError:
    abc = collections
'''
            header += r'''
object = object
int = int
set = set
frozenset = frozenset
tuple = tuple
list = list
len = len
isinstance = isinstance
getattr = getattr
slice = slice

def recursive(func):
    """Tail recursion optimizer."""
    state = [True, None] # toplevel, (args, kwargs)
    recurse = object()
    @functools.wraps(func)
    def tailed_func(*args, **kwargs):
        """Tail Recursion Wrapper."""
        if state[0]:
            state[0] = False
            try:
                while True:
                    result = func(*args, **kwargs)
                    if result is recurse:
                        args, kwargs = state[1]
                        state[1] = None
                    else:
                        return result
            finally:
                state[0] = True
        else:
            state[1] = args, kwargs
            return recurse
    return tailed_func

class MatchError(Exception):
    """Pattern-matching error."""
'''
        else:
            if which == "module":
                header += r'''
import sys as _coconut_sys
import os.path as _coconut_os_path
_coconut_sys.path.append(_coconut_os_path.dirname(_coconut_os_path.abspath(__file__)))
import __coconut__
'''
            elif which == "code" or which == "file":
                header += r'''
class __coconut__(object):
    """Built-in Coconut functions."""
    version = "'''+VERSION+r'''"
    import functools
    import operator
    import itertools
    import collections
'''
                if version == "2":
                    header += r'''    abc = collections'''
                elif version == "3":
                    header += r'''    import collections.abc as abc'''
                else:
                    header += r'''    try:
        import collections.abc as abc
    except ImportError:
        abc = collections'''
                header += r'''
    object = object
    int = int
    set = set
    frozenset = frozenset
    tuple = tuple
    list = list
    len = len
    isinstance = isinstance
    getattr = getattr
    slice = slice
    @staticmethod
    def recursive(func):
        """Tail recursion optimizer."""
        state = [True, None] # toplevel, (args, kwargs)
        recurse = object()
        @__coconut__.functools.wraps(func)
        def tailed_func(*args, **kwargs):
            """Tail Recursion Wrapper."""
            if state[0]:
                state[0] = False
                try:
                    while True:
                        result = func(*args, **kwargs)
                        if result is recurse:
                            args, kwargs = state[1]
                            state[1] = None
                        else:
                            return result
                finally:
                    state[0] = True
            else:
                state[1] = args, kwargs
                return recurse
        return tailed_func
    class MatchError(Exception):
        """Pattern-matching error."""
'''
            else:
                raise CoconutException("invalid header type: "+repr(which))
            header += r'''
__coconut_version__ = __coconut__.version
reduce = __coconut__.functools.reduce
itemgetter = __coconut__.operator.itemgetter
attrgetter = __coconut__.operator.attrgetter
methodcaller = __coconut__.operator.methodcaller
takewhile = __coconut__.itertools.takewhile
dropwhile = __coconut__.itertools.dropwhile
tee = __coconut__.itertools.tee
recursive = __coconut__.recursive
MatchError = __coconut__.MatchError
'''
            if which != "code":
                header += r'''
# Compiled Coconut: ------------------------------------------------------------

'''
    return header

#-----------------------------------------------------------------------------------------------------------------------
# CONSTANTS:
#-----------------------------------------------------------------------------------------------------------------------

ParserElement.enablePackrat()

openstr = "\u204b"
closestr = "\xb6"
linebreak = "\n"
white = " \t\f"
downs = "([{"
ups = ")]}"
holds = "'\""
startcomment = "#"
endline = "\n\r"
escape = "\\"
tablen = 4
decorator_var = "_coconut_decorator"
match_to_var = "_coconut_match_to"
match_check_var = "_coconut_match_check"
match_iter_var = "_coconut_match_iter"
match_err_var = "_coconut_match_err"
lazy_item_var = "_coconut_lazy_item"
wildcard = "_"
keywords = ["and",
            "as",
            "as",
            "assert",
            "break",
            "class",
            "continue",
            "def",
            "del",
            "elif",
            "else",
            "except",
            "finally",
            "for",
            "from",
            "global",
            "if",
            "import",
            "in",
            "is",
            "lambda",
            "not",
            "or",
            "pass",
            "raise",
            "return",
            "try",
            "while",
            "with",
            "yield"]
const_vars = ["True", "False", "None"]
reserved_vars = ["nonlocal", "data", "match", "case", "async", "await"]

ParserElement.setDefaultWhitespaceChars(white)

#-----------------------------------------------------------------------------------------------------------------------
# UTILITIES:
#-----------------------------------------------------------------------------------------------------------------------

def clean(line):
    """Cleans a line."""
    return line.replace(openstr, "").replace(closestr, "").strip()

class CoconutException(Exception):
    """Base Coconut exception."""
    def __init__(self, value):
        """creates the Coconut exception."""
        self.value = value
    def __repr__(self):
        """Displays the Coconut exception."""
        return self.value
    def __str__(self):
        """Wraps repr."""
        return repr(self)

class CoconutSyntaxError(CoconutException):
    """Coconut SyntaxError."""
    def __init__(self, message, source, point=None):
        """Creates the Coconut SyntaxError."""
        self.value = message
        if point is None:
            self.value += linebreak + "  " + source
        else:
            if point >= len(source):
                point = len(source)-1
            part = source.splitlines()[lineno(point, source)-1]
            self.value += linebreak + "  " + part + linebreak + "  "
            for x in range(0, col(point, source)-1):
                if part[x] in white:
                    self.value += part[x]
                else:
                    self.value += " "
            self.value += "^"

class CoconutParseError(CoconutSyntaxError):
    """Coconut ParseError."""
    def __init__(self, line, col, lineno):
        """Creates The Coconut ParseError."""
        super(CoconutParseError, self).__init__("parsing failed in line "+str(lineno), clean(line), col-1)

class CoconutStyleError(CoconutSyntaxError):
    """Coconut --strict error."""
    def __init__(self, message, source, point=None):
        """Creates the --strict Coconut error."""
        message += " (disable --strict to dismiss)"
        super(CoconutStyleError, self).__init__(message, source, point)

class CoconutTargetError(CoconutSyntaxError):
    """Coconut --target error."""
    def __init__(self, message, source, point=None):
        """Creates the --target Coconut error."""
        message += " (enable --target 3 to dismiss)"
        super(CoconutTargetError, self).__init__(message, source, point)

def attach(item, action):
    """Attaches a parse action to an item."""
    return item.copy().addParseAction(action)

def fixto(item, output):
    """Forces an item to result in a specific output."""
    return attach(item, replaceWith(output))

def addspace(item):
    """Condenses and adds space to the tokenized output."""
    def callback(tokens):
        """Callback function constructed by addspace."""
        return " ".join(tokens)
    return attach(item, callback)

def condense(item):
    """Condenses the tokenized output."""
    def callback(tokens):
        """Callback function constructed by condense."""
        return "".join(tokens)
    return attach(item, callback)

def parenwrap(lparen, item, rparen):
    """Wraps an item in optional parentheses."""
    return condense(lparen.suppress() + item + rparen.suppress() ^ item)

class tracer(object):
    """Debug tracer."""
    show = print

    def __init__(self, on=False):
        """Creates the tracer."""
        self.debug(on)

    def debug(self, on=True):
        """Changes the tracer's state."""
        self.on = on

    def trace(self, original, location, tokens, message=None):
        """Tracer parse action."""
        if self.on:
            original = str(original)
            location = int(location)
            out = ""
            if message is not None:
                out += "["+message+"] "
            if len(tokens) == 1 and isinstance(tokens[0], str):
                out += repr(tokens[0])
            else:
                out += str(tokens)
            out += " (line "+str(lineno(location, original))+", col "+str(col(location, original))+")"
            self.show(out)
        return tokens

    def bind(self, item, message=None):
        """Traces a parse element."""
        if message is None:
            callback = self.trace
        else:
            def callback(original, location, tokens):
                """Callback function constructed by tracer."""
                return self.trace(original, location, tokens, message)
        bound = attach(item, callback)
        if message is not None:
            bound.setName(message)
        return bound

#-----------------------------------------------------------------------------------------------------------------------
# PROCESSORS:
#-----------------------------------------------------------------------------------------------------------------------

def anyint_proc(tokens):
    """Replaces underscored integers."""
    if len(tokens) == 1:
        base, item = tokens[0].split("_")
        return '__coconut__.int("'+item+'", '+base+")"
    else:
        raise CoconutException("invalid anyint tokens: "+repr(tokens))

def list_proc(tokens):
    """Properly formats lists."""
    out = []
    for x in range(0, len(tokens)):
        if x%2 == 0:
            out.append(tokens[x])
        else:
            out[-1] += tokens[x]
    return " ".join(out)

def itemlist(item, sep):
    """Creates a list containing an item."""
    return attach(item + ZeroOrMore(sep + item) + Optional(sep), list_proc)

def attr_proc(tokens):
    """Processes attrgetter literals."""
    if len(tokens) == 1:
        return '__coconut__.operator.attrgetter("'+tokens[0]+'")'
    else:
        raise CoconutException("invalid attrgetter literal tokens: "+repr(tokens))

def item_proc(tokens):
    """Processes items."""
    out = tokens.pop(0)
    for trailer in tokens:
        if isinstance(trailer, str):
            out += trailer
        elif len(trailer) == 1:
            if trailer[0] == "$[]":
                out = ("(lambda i: __coconut__.itertools.islice("+out+", i.start, i.stop, i.step) if isinstance(i, __coconut__.slice)"
                       " else next(__coconut__.itertools.islice("+out+", i, i+1)))")
            elif trailer[0] == "$":
                out = "__coconut__.functools.partial(__coconut__.functools.partial, "+out+")"
            elif trailer[0] == "[]":
                out = "__coconut__.functools.partial(__coconut__.operator.__getitem__, "+out+")"
            elif trailer[0] == ".":
                out = "__coconut__.functools.partial(__coconut__.getattr, "+out+")"
            else:
                raise CoconutSyntaxError("an argument is required", trailer[0])
        elif len(trailer) == 2:
            if trailer[0] == "$(":
                out = "__coconut__.functools.partial("+out+", "+trailer[1]+")"
            elif trailer[0] == "$[":
                if 0 < len(trailer[1]) <= 3:
                    args = []
                    for x in range(0, len(trailer[1])):
                        arg = trailer[1][x]
                        if not arg:
                            if x == 0:
                                arg = "0"
                            else:
                                arg = "None"
                        args.append(arg)
                    out = "__coconut__.itertools.islice("+out
                    if len(args) == 1:
                        out += ", "+args[0]+", ("+args[0]+") + 1)"
                        out = "next("+out+")"
                    else:
                        for arg in args:
                            out += ", "+arg
                        out += ")"
                else:
                    raise CoconutException("invalid iterator slice args: "+repr(trailer[1]))
            elif trailer[0] == "..":
                out = "(lambda *args, **kwargs: "+out+"(("+trailer[1]+")(*args, **kwargs)))"
            else:
                raise CoconutException("invalid special trailer: "+repr(trailer[0]))
        else:
            raise CoconutException("invalid trailer tokens: "+repr(trailer))
    return out

def lazy_list_proc(tokens):
    """Processes lazy lists."""
    return (
        "(" + lazy_item_var + "() for " + lazy_item_var + " in ("
            + ("lambda: " if len(tokens) != 0 else "")
            + ", lambda: ".join(tokens) + ("," if len(tokens) == 1 else "")
        + "))"
    )

def chain_proc(tokens):
    """Processes chain calls."""
    if len(tokens) == 1:
        return tokens[0]
    else:
        return "__coconut__.itertools.chain.from_iterable(" + lazy_list_proc(tokens) + ")"

def get_infix_items(tokens):
    """Performs infix token processing."""
    if len(tokens) < 3:
        raise CoconutException("invalid infix tokens: "+repr(tokens))
    else:
        items = []
        for item in tokens[0]:
            items.append(item)
        for item in tokens[2]:
            items.append(item)
        if len(tokens) > 3:
            items.append(infix_proc([[]]+tokens[3:]))
        args = []
        for arg in items:
            if arg:
                args.append(arg)
        return tokens[1], args

def infix_proc(tokens):
    """Processes infix calls."""
    func, args = get_infix_items(tokens)
    return "("+func+")("+", ".join(args)+")"

def op_funcdef_proc(tokens):
    """Processes infix defs."""
    func, args = get_infix_items(tokens)
    return func+"("+", ".join(args)+")"

def pipe_proc(tokens):
    """Processes pipe calls."""
    if len(tokens) == 1:
        return tokens[0]
    else:
        func = tokens.pop()
        op = tokens.pop()
        if op == "|>":
            return "("+func+")("+pipe_proc(tokens)+")"
        elif op == "|*>":
            return "("+func+")(*"+pipe_proc(tokens)+")"
        elif op == "<|":
            return "("+pipe_proc(tokens)+")("+func+")"
        elif op == "<*|":
            return "("+pipe_proc(tokens)+")(*"+func+")"
        else:
            raise CoconutException("invalid pipe operator: "+op)

def lambdef_proc(tokens):
    """Processes lambda calls."""
    if len(tokens) == 1:
        return "lambda: "+tokens[0]
    elif len(tokens) == 2:
        return "lambda "+tokens[0]+": "+tokens[1]
    else:
        raise CoconutException("invalid lambda tokens: "+repr(tokens))

def assign_proc(tokens):
    """Processes assignments."""
    if len(tokens) == 3:
        name, op, item = tokens
        item = "(" + item + ")"
        out = ""
        if op == "|>=":
            out += name+" = "+item+"("+name+")"
        elif op == "|*>=":
            out += name+" = "+item+"(*"+name+")"
        elif op == "<|=":
            out += name+" = "+name+"("+item+")"
        elif op == "<*|=":
            out += name+" = "+name+"(*"+item+")"
        elif op == "..=":
            out += name+" = (lambda f, g: lambda *args, **kwargs: f(g(*args, **kwargs)))("+name+", "+item+")"
        elif op == "::=":
            out += name+" = __coconut__.itertools.chain("+name+", "+item+")"
        else:
            out += name+" "+op+" "+item
        return out
    else:
        raise CoconutException("invalid assignment tokens: "+repr(tokens))

def func_proc(tokens):
    """Processes mathematical function definitons."""
    if len(tokens) == 2:
        return "def " + tokens[0] + ": return " + tokens[1]
    else:
        raise CoconutException("invalid mathematical function definition tokens: "+repr(tokens))

def match_func_proc(tokens):
    """Processes match mathematical function definitions."""
    if len(tokens) == 2:
        return tokens[0] + "return " + tokens[1] + linebreak + closestr
    else:
        raise CoconutException("invalid pattern-matching mathematical function definition tokens: "+repr(tokens))

def full_match_funcdef_proc(tokens):
    """Processes full match function definition."""
    if len(tokens) == 2:
        return tokens[0] + "".join(tokens[1]) + closestr
    else:
        raise CoconutException("invalid pattern-matching function definition tokens: "+repr(tokens))

def data_proc(tokens):
    """Processes data blocks."""
    if len(tokens) == 2:
        return "class "+tokens[0]+'(__coconut__.collections.namedtuple("'+tokens[0]+'", "'+tokens[1]+'"))'
    elif len(tokens) == 1:
        return "class "+tokens[0]+'(__coconut__.collections.namedtuple("'+tokens[0]+'", ""))'
    else:
        raise CoconutException("invalid data tokens: "+repr(tokens))

def decorator_proc(tokens):
    """Processes decorators."""
    defs = []
    decorates = []
    for x in range(0, len(tokens)):
        varname = decorator_var + "_" + str(x)
        defs.append(varname+" = "+tokens[x])
        decorates.append("@"+varname)
    return linebreak.join(defs + decorates) + linebreak

def else_proc(tokens):
    """Processes compound else statements."""
    if len(tokens) == 1:
        return linebreak + openstr + tokens[0] + closestr
    else:
        raise CoconutException("invalid compound else statement tokens: "+repr(tokens))

def set_proc(tokens):
    """Processes set literals."""
    if len(tokens) == 1:
        set_type = tokens[0]
        if set_type == "s":
            return "__coconut__.set()"
        elif set_type == "f":
            return "__coconut__.frozenset()"
        else:
            raise CoconutException("invalid set type: "+str(set_type))
    elif len(tokens) == 2:
        set_type, set_maker = tokens
        if set_type == "s":
            return "__coconut__.set(["+set_maker+"])"
        elif set_type == "f":
            return "__coconut__.frozenset(["+set_maker+"])"
        else:
            raise CoconutException("invalid set type: "+str(set_type))
    else:
        raise CoconutException("invalid set literal tokens: "+repr(tokens))

def class_proc(tokens):
    """Processes class inheritance lists."""
    if len(tokens) == 0:
        return "(__coconut__.object)"
    elif len(tokens) == 1:
        return "("+tokens[0]+")"
    else:
        raise CoconutException("invalid class inheritance tokens: "+repr(tokens))

class matcher(object):
    """Pattern-matching processor."""
    position = 0
    iter_index = 0

    def __init__(self, checkvar, checkdefs=None, names=None):
        """Creates the matcher."""
        self.setup()
        self.checkvar = checkvar
        self.checkdefs = []
        if checkdefs is None:
            self.increment()
        else:
            for checks, defs in checkdefs:
                self.checkdefs.append([checks[:], defs[:]])
            self.checks = self.get_checks(-1)
            self.defs = self.get_defs(-1)
        if names is None:
            self.names = {}
        else:
            self.names = dict(names)
        self.others = []

    def setup(self):
        """Sets up match functions."""
        self.matchers = {
            "dict": self.match_dict,
            "iter": self.match_iterator,
            "series": self.match_sequence,
            "rseries": self.match_rsequence,
            "mseries": self.match_msequence,
            "const": self.match_const,
            "is": self.match_typedef,
            "var": self.match_var,
            "set": self.match_set,
            "data": self.match_data,
            "paren": self.match_paren,
            "assign": self.match_assign,
            "and": self.match_and,
            "or": self.match_or
        }

    def duplicate(self):
        """Duplicates the matcher to others."""
        self.others.append(matcher(self.checkvar, self.checkdefs, self.names))
        self.others[-1].set_checks(0, ["not "+self.checkvar] + self.others[-1].get_checks(0))
        return self.others[-1]

    def get_checks(self, position):
        """Gets the checks at the position."""
        return self.checkdefs[position][0]

    def set_checks(self, position, checks):
        """Sets the checks at the position."""
        self.checkdefs[position][0] = checks

    def set_defs(self, position, defs):
        """Sets the defs at the position."""
        self.checkdefs[position][1] = defs

    def get_defs(self, position):
        """Gets the defs at the position."""
        return self.checkdefs[position][1]

    def add_check(self, check_item):
        """Adds a check universally."""
        self.checks.append(check_item)
        for other in self.others:
            other.add_check(check_item)

    def add_def(self, def_item):
        """Adds a def universally."""
        self.defs.append(def_item)
        for other in self.others:
            other.add_def(def_item)

    def set_position(self, position):
        """Sets the if-statement position."""
        if position > 0:
            while position >= len(self.checkdefs):
                self.checkdefs.append([[], []])
            self.checks = self.checkdefs[position][0]
            self.defs = self.checkdefs[position][1]
            self.position = position
        else:
            raise CoconutException("invalid match index: "+str(position))

    def increment(self, forall=False):
        """Advances the if-statement position."""
        self.set_position(self.position+1)
        if forall:
            for other in self.others:
                other.increment(True)

    def decrement(self, forall=False):
        """Decrements the if-statement position."""
        self.set_position(self.position-1)
        if forall:
            for other in self.others:
                other.decrement(True)

    def match_dict(self, original, item):
        """Matches a dictionary."""
        if len(original) == 1:
            match = original[0]
        else:
            raise CoconutException("invalid dict match tokens: "+repr(original))
        self.checks.append("__coconut__.isinstance("+item+", __coconut__.abc.Mapping)")
        self.checks.append("__coconut__.len("+item+") == "+str(len(match)))
        for x in range(0, len(match)):
            k,v = match[x]
            self.checks.append(k+" in "+item)
            self.match(v, item+"["+k+"]")

    def match_sequence(self, original, item):
        """Matches a sequence."""
        tail = None
        if len(original) == 2:
            series_type, match = original
        else:
            series_type, match, tail = original
        self.checks.append("__coconut__.isinstance("+item+", __coconut__.abc.Sequence)")
        if tail is None:
            self.checks.append("__coconut__.len("+item+") == "+str(len(match)))
        else:
            self.checks.append("__coconut__.len("+item+") >= "+str(len(match)))
            if len(match):
                splice = "["+str(len(match))+":]"
            else:
                splice = ""
            if series_type == "(":
                self.defs.append(tail+" = __coconut__.tuple("+item+splice+")")
            elif series_type == "[":
                self.defs.append(tail+" = __coconut__.list("+item+splice+")")
            else:
                raise CoconutException("invalid series match type: "+repr(series_type))
        for x in range(0, len(match)):
            self.match(match[x], item+"["+str(x)+"]")

    def match_iterator(self, original, item):
        """Matches an iterator."""
        tail = None
        if len(original) == 2:
            _, match = original
        else:
            _, match, tail = original
        self.checks.append("__coconut__.isinstance("+item+", __coconut__.abc.Iterable)")
        itervar = match_iter_var + "_" + str(self.iter_index)
        self.iter_index += 1
        if tail is None:
            self.defs.append(itervar+" = __coconut__.tuple("+item+")")
        else:
            self.defs.append(itervar+" = __coconut__.tuple(__coconut__.itertools.islice("+item+", 0, "+str(len(match))+"))")
            self.defs.append(tail+" = "+item)
        self.increment()
        if tail is None:
            self.checks.append("__coconut__.len("+itervar+") == "+str(len(match)))
        else:
            self.checks.append("__coconut__.len("+itervar+") >= "+str(len(match)))
        for x in range(0, len(match)):
            self.match(match[x], itervar+"["+str(x)+"]")
        self.decrement()

    def match_rsequence(self, original, item):
        """Matches a reverse sequence."""
        front, series_type, match = original
        self.checks.append("__coconut__.isinstance("+item+", __coconut__.abc.Sequence)")
        self.checks.append("__coconut__.len("+item+") >= "+str(len(match)))
        if len(match):
            splice = "[:"+str(-len(match))+"]"
        else:
            splice = ""
        if series_type == "(":
            self.defs.append(front+" = __coconut__.tuple("+item+splice+")")
        elif series_type == "[":
            self.defs.append(front+" = __coconut__.list("+item+splice+")")
        else:
            raise CoconutException("invalid series match type: "+repr(series_type))
        for x in range(0, len(match)):
            self.match(match[x], item+"["+str(x - len(match))+"]")

    def match_msequence(self, original, item):
        """Matches a middle sequence."""
        series_type, head_match, middle, _, last_match = original
        self.checks.append("__coconut__.isinstance("+item+", __coconut__.abc.Sequence)")
        self.checks.append("__coconut__.len("+item+") >= "+str(len(head_match) + len(last_match)))
        if len(head_match) and len(last_match):
            splice = "["+str(len(head_match))+":"+str(-len(last_match))+"]"
        elif len(head_match):
            splice = "["+str(len(head_match))+":]"
        elif len(last_match):
            splice = "[:"+str(-len(last_match))+"]"
        else:
            splice = ""
        if series_type == "(":
            self.defs.append(middle+" = __coconut__.tuple("+item+splice+")")
        elif series_type == "[":
            self.defs.append(middle+" = __coconut__.list("+item+splice+")")
        else:
            raise CoconutException("invalid series match type: "+repr(series_type))
        for x in range(0, len(head_match)):
            self.match(head_match[x], item+"["+str(x)+"]")
        for x in range(0, len(last_match)):
            self.match(last_match[x], item+"["+str(x - len(last_match))+"]")

    def match_const(self, original, item):
        """Matches a constant."""
        (match,) = original
        if match in const_vars:
            self.checks.append(item+" is "+match)
        else:
            self.checks.append(item+" == "+match)

    def match_typedef(self, original, item):
        """Matches a typedef."""
        match, type_check = original
        self.checks.append("__coconut__.isinstance("+item+", ("+type_check+"))")
        self.match(match, item)

    def match_var(self, original, item):
        """Matches a variable."""
        (setvar,) = original
        if setvar != wildcard:
            if setvar in self.names:
                self.checks.append(self.names[setvar]+" == "+item)
            else:
                self.defs.append(setvar+" = "+item)
                self.names[setvar] = item

    def match_set(self, original, item):
        """Matches a set."""
        if len(original) == 1:
            match = original[0]
        else:
            raise CoconutException("invalid set match tokens: "+repr(original))
        self.checks.append("__coconut__.isinstance("+item+", __coconut__.abc.Set)")
        self.checks.append("__coconut__.len("+item+") == "+str(len(match)))
        for const in match:
            self.checks.append(const+" in "+item)

    def match_data(self, original, item):
        """Matches a data type."""
        data_type, match = original
        self.checks.append("__coconut__.isinstance("+item+", "+data_type+")")
        self.checks.append("__coconut__.len("+item+") == "+str(len(match)))
        for x in range(0, len(match)):
            self.match(match[x], item+"["+str(x)+"]")

    def match_paren(self, original, item):
        """Matches a paren."""
        (match,) = original
        self.match(match, item)

    def match_assign(self, original, item):
        """Matches assignment."""
        setvar, match = original
        if setvar in self.names:
            self.checks.append(self.names[setvar]+" == "+item)
        elif setvar != wildcard:
            self.defs.append(setvar+" = "+item)
            self.names[setvar] = item
        self.match(match, item)

    def match_and(self, original, item):
        """Matches and."""
        for match in original:
            self.match(match, item)

    def match_or(self, original, item):
        """Matches or."""
        for x in range(1, len(original)):
            self.duplicate().match(original[x], item)
        self.match(original[0], item)

    def match(self, original, item):
        """Performs pattern-matching processing."""
        for flag in self.matchers:
            if flag in original:
                return self.matchers[flag](original, item)
        raise CoconutException("invalid inner match tokens: "+repr(original))

    def out(self):
        out = ""
        closes = 0
        for checks, defs in self.checkdefs:
            if checks:
                out += "if (" + ") and (".join(checks) + "):" + linebreak + openstr
                closes += 1
            if defs:
                out += linebreak.join(defs) + linebreak
        out += self.checkvar + " = True" + linebreak
        out += closestr * closes
        for other in self.others:
            out += other.out()
        return out

def match_proc(tokens):
    """Processes match blocks."""
    if len(tokens) == 3:
        matches, item, stmts = tokens
        cond = None
    elif len(tokens) == 4:
        matches, item, cond, stmts = tokens
    else:
        raise CoconutException("invalid outer match tokens: "+repr(tokens))
    matching = matcher(match_check_var)
    matching.match(matches, match_to_var)
    if cond:
        matching.increment(True)
        matching.add_check(cond)
    out = match_check_var + " = False" + linebreak
    out += match_to_var + " = " + item + linebreak
    out += matching.out()
    if stmts is not None:
        out += "if "+match_check_var+":" + linebreak + openstr + "".join(stmts) + closestr
    return out

def pattern_error(original, loc):
    """Constructs a pattern-matching error message."""
    match_line = repr(clean(line(loc, original)))
    return ("if not " + match_check_var + ":" + linebreak + openstr
        + match_err_var + ' = __coconut__.MatchError("pattern-matching failed for " '
        + repr(match_line) + ' " in " + repr(repr(' + match_to_var + ")))"
        + linebreak + match_err_var + ".pattern = " + match_line
        + linebreak + match_err_var + ".value = " + match_to_var
        + linebreak + "raise " + match_err_var
        + linebreak + closestr)

def match_assign_proc(original, loc, tokens):
    """Processes match assign blocks."""
    matches, item = tokens
    out = match_proc((matches, item, None))
    out += pattern_error(original, loc)
    return out

def case_to_match(tokens, item):
    """Converts case tokens to match tokens."""
    if len(tokens) == 2:
        matches, stmts = tokens
        return matches, item, stmts
    elif len(tokens) == 3:
        matches, cond, stmts = tokens
        return matches, item, cond, stmts
    else:
        raise CoconutException("invalid case match tokens: "+repr(tokens))

def case_proc(tokens):
    """Processes case blocks."""
    if len(tokens) == 2:
        item, cases = tokens
        default = None
    elif len(tokens) == 3:
        item, cases, default = tokens
    else:
        raise CoconutException("invalid top-level case tokens: "+repr(tokens))
    out = match_proc(case_to_match(cases[0], item))
    for case in cases[1:]:
        out += ("if not "+match_check_var+":" + linebreak + openstr
            + match_proc(case_to_match(case, item)) + closestr)
    if default is not None:
        out += "if not "+match_check_var+default
    return out

def name_match_funcdef_proc(original, loc, tokens):
    """Processes match defs."""
    func, matches = tokens
    matching = matcher(match_check_var)
    matching.match_sequence(("(", matches), match_to_var)
    out = "def " + func + " (*" + match_to_var + "):" + linebreak + openstr
    out += match_check_var + " = False" + linebreak
    out += matching.out()
    out += pattern_error(original, loc)
    return out

def op_match_funcdef_proc(original, loc, tokens):
    """Processes infix match defs."""
    return name_match_funcdef_proc(original, loc, get_infix_items(tokens))

def except_proc(tokens):
    """Processes except statements."""
    if len(tokens) == 1:
        return "except ("+tokens[0]+")"
    elif len(tokens) == 2:
        return "except ("+tokens[0]+") as "+tokens[1]
    else:
        raise CoconutException("invalid except tokens: "+repr(tokens))

#-----------------------------------------------------------------------------------------------------------------------
# PARSER:
#-----------------------------------------------------------------------------------------------------------------------

class processor(object):
    """The Coconut processor."""
    TRACER = tracer()
    trace = TRACER.bind
    debug = TRACER.debug
    versions = [None, "2", "3"]

    def __init__(self, strict=False, version=None):
        """Creates a new processor."""
        if version in self.versions:
            self.version = version
        else:
            raise CoconutException("unsupported target Python version " + repr(version)
                + " (supported targets are '2' and '3', or leave blank for universal)")
        self.strict = strict
        self.bind()
        self.setup()
        self.clean()

    def bind(self):
        """Binds reference objects to the proper parse actions."""
        self.string_ref <<= self.trace(attach(self.string_marker, self.string_repl), "string_ref")
        self.moduledoc <<= self.trace(attach(self.string_marker + self.newline, self.set_docstring), "moduledoc")
        self.comment <<= self.trace(attach(self.comment_marker, self.comment_repl), "comment")
        self.passthrough <<= self.trace(attach(self.passthrough_marker, self.passthrough_repl), "passthrough")
        self.passthrough_block <<= self.trace(attach(self.passthrough_block_marker, self.passthrough_repl), "passthrough_block")
        self.u_string_ref <<= attach(self.u_string, self.u_string_check)
        self.typedef_ref <<= attach(self.typedef, self.typedef_check)
        self.return_typedef_ref <<= attach(self.return_typedef, self.typedef_check)
        self.yield_from_ref <<= attach(self.yield_from, self.yield_from_check)
        self.matrix_at_ref <<= attach(self.matrix_at, self.matrix_at_check)
        self.nonlocal_stmt_ref <<= attach(self.nonlocal_stmt, self.nonlocal_check)
        self.dict_comp_ref <<= attach(self.dict_comp, self.dict_comp_check)
        self.star_assign_item_ref <<= attach(self.star_assign_item, self.star_assign_item_check)
        self.classic_lambdef_ref <<= attach(self.classic_lambdef, self.lambdef_check)
        self.classic_lambdef_nocond_ref <<= attach(self.classic_lambdef_nocond, self.lambdef_check)
        self.set_literal_ref <<= attach(self.set_literal, self.set_literal_convert)
        self.async_funcdef_ref <<= attach(self.async_funcdef, self.async_stmt_check)
        self.async_match_funcdef_ref <<= attach(self.async_match_funcdef, self.async_stmt_check)
        self.async_block_ref <<= attach(self.async_block, self.async_stmt_check)
        self.await_keyword_ref <<= attach(self.await_keyword, self.await_keyword_check)
        self.complex_raise_stmt_ref <<= attach(self.complex_raise_stmt, self.complex_raise_stmt_check)

    def setup(self):
        """Initializes the processor."""
        self.preprocs = [self.prepare, self.str_proc, self.passthrough_proc, self.ind_proc]
        self.postprocs = [self.reind_proc, self.header_proc]

    def clean(self):
        """Resets references."""
        self.indchar = None
        self.refs = []
        self.docstring = ""

    def wrap_str(self, text, strchar, multiline):
        """Wraps a string."""
        self.refs.append((text, strchar, multiline))
        return '"'+str(len(self.refs)-1)+'"'

    def wrap_passthrough(self, text, multiline):
        """Wraps a passthrough."""
        if not multiline:
            text = text.lstrip()
        fulltext = ""
        found = None
        for c in text:
            if found is not None:
                if c == '"':
                    fulltext += self.string_repl([found])
                    found = None
                else:
                    found += c
            elif c == '"':
                found = ""
            else:
                fulltext += c
        self.refs.append(fulltext)
        if multiline:
            out = "\\"
        else:
            out = "\\\\"
        out += str(len(self.refs)-1)
        if not multiline:
            out += linebreak
        return out

    def wrap_comment(self, text):
        """Wraps a comment."""
        self.refs.append(text)
        return "#"+str(len(self.refs)-1)

    def prepare(self, inputstring, strip=False, **kwargs):
        """Prepares a string for processing."""
        if strip:
            return inputstring.strip()
        else:
            return inputstring

    def str_proc(self, inputstring, **kwargs):
        """Processes strings."""
        out = []
        found = None
        hold = None
        _comment = 0
        _char = 0
        _start = 1
        _store = 2
        x = 0
        while x <= len(inputstring):
            if x == len(inputstring):
                c = linebreak
            else:
                c = inputstring[x]
            if hold is not None:
                if len(hold) == 1:
                    if c in endline:
                        out.append(self.wrap_comment(hold[_comment])+c)
                        hold = None
                    else:
                        hold[_comment] += c
                elif hold[_store] is not None:
                    if c == escape:
                        hold[_char] += hold[_store]+c
                        hold[_store] = None
                    elif c == hold[_start][0]:
                        hold[_store] += c
                    elif len(hold[_store]) > len(hold[_start]):
                        raise CoconutSyntaxError("invalid number of string closes", inputstring, x)
                    elif hold[_store] == hold[_start]:
                        out.append(self.wrap_str(hold[_char], hold[_start][0], True))
                        hold = None
                        x -= 1
                    else:
                        hold[_char] += hold[_store]+c
                        hold[_store] = None
                elif hold[_char].endswith(escape) and not hold[_char].endswith(escape*2):
                    hold[_char] += c
                elif c == hold[_start]:
                    out.append(self.wrap_str(hold[_char], hold[_start], False))
                    hold = None
                elif c == hold[_start][0]:
                    hold[_store] = c
                elif len(hold[_start]) == 1 and c in endline:
                    raise CoconutSyntaxError("linebreak in non-multiline string", inputstring, x)
                else:
                    hold[_char] += c
            elif found is not None:
                if c == found[0]:
                    found += c
                elif len(found) == 1:
                    if c in endline:
                        raise CoconutSyntaxError("linebreak in non-multiline string", inputstring, x)
                    else:
                        hold = [c, found, None] # [_char, _start, _store]
                        found = None
                elif len(found) == 2:
                    out.append(self.wrap_str("", found[0], False))
                    found = None
                    x -= 1
                elif len(found) == 3:
                    hold = [c, found, None] # [_char, _start, _store]
                    found = None
                else:
                    raise CoconutSyntaxError("invalid number of string starts", inputstring, x)
            elif c in startcomment:
                hold = [""] # [_comment]
            elif c in holds:
                found = c
            else:
                out.append(c)
            x += 1
        if hold is not None or found is not None:
            raise CoconutSyntaxError("unclosed string", inputstring, x)
        else:
            return "".join(out)

    def passthrough_proc(self, inputstring, **kwargs):
        """Processes python passthroughs."""
        out = []
        found = None
        hold = None
        count = None
        multiline = None
        for x in range(0, len(inputstring)):
            c = inputstring[x]
            if hold is not None:
                count += self.change(c)
                if count >= 0 and c in hold:
                    out.append(self.wrap_passthrough(found, multiline))
                    found = None
                    hold = None
                    count = None
                    multiline = None
                else:
                    found += c
            elif found:
                if c == escape:
                    found = ""
                    hold = endline
                    count = 0
                    multiline = False
                elif c == "(":
                    found = ""
                    hold = ")"
                    count = -1
                    multiline = True
                else:
                    out.append(escape + c)
                    found = None
            elif c == escape:
                found = True
            else:
                out.append(c)
        if hold is not None or found is not None:
            raise CoconutSyntaxError("unclosed passthrough", inputstring, x)
        else:
            return "".join(out)

    def leading(self, inputstring):
        """Counts leading whitespace."""
        count = 0
        for x in range(0, len(inputstring)):
            if inputstring[x] == " ":
                if self.indchar is None:
                    self.indchar = " "
                count += 1
            elif inputstring[x] == "\t":
                if self.indchar is None:
                    self.indchar = "\t"
                count += tablen - x % tablen
            else:
                break
            if self.strict and self.indchar != inputstring[x]:
                raise CoconutStyleError("found mixing of tabs and spaces", inputstring, x)
        return count

    def change(self, inputstring):
        """Determines the parenthetical change of level."""
        count = 0
        for c in inputstring:
            if c in downs:
                count -= 1
            elif c in ups:
                count += 1
        return count

    def ind_proc(self, inputstring, **kwargs):
        """Processes indentation."""
        lines = inputstring.splitlines()
        new = []
        levels = []
        count = 0
        current = None
        for line in lines:
            if line and line[-1] in white:
                if self.strict:
                    raise CoconutStyleError("found trailing whitespace", line)
                else:
                    line = line.rstrip()
            if new:
                last = new[-1].split(startcomment, 1)[0].rstrip()
            else:
                last = None
            if not line or line.lstrip().startswith(startcomment):
                if count >= 0:
                    new.append(line)
            elif last is not None and last.endswith("\\"):
                if self.strict:
                    raise CoconutStyleError("found backslash continuation", last)
                else:
                    new[-1] = last[:-1]+" "+line
            elif count < 0:
                new[-1] = last+" "+line
            else:
                check = self.leading(line)
                if current is None:
                    if check:
                        raise CoconutSyntaxError("illegal initial indent", line)
                    else:
                        current = 0
                elif check > current:
                    levels.append(current)
                    current = check
                    line = openstr+line
                elif check in levels:
                    point = levels.index(check)+1
                    line = closestr*(len(levels[point:])+1)+line
                    levels = levels[:point]
                    current = levels.pop()
                elif current != check:
                    raise CoconutSyntaxError("illegal dedent to unused indentation level", line)
                new.append(line)
            count += self.change(line)
        if new:
            last = new[-1].split(startcomment, 1)[0].rstrip()
            if last.endswith("\\"):
                raise CoconutSyntaxError("illegal final backslash continuation", last)
            if count != 0:
                raise CoconutSyntaxError("unclosed parenthetical", new[-1])
        new.append(closestr*len(levels))
        return linebreak.join(new)

    def reindent(self, inputstring):
        """Reconverts indent tokens into indentation."""
        out = []
        level = 0
        hold = None
        _char = 0
        _escape = 1
        for line in inputstring.splitlines():
            line = line.strip()
            if hold is None and not line.startswith(startcomment):
                while line.startswith(openstr) or line.startswith(closestr):
                    if line[0] == openstr:
                        level += 1
                    elif line[0] == closestr:
                        level -= 1
                    line = line[1:]
                line = " "*tablen*level + line
            for c in line:
                if hold:
                    if c == escape:
                        hold[_escape] = not hold[_escape]
                    elif hold[_escape]:
                        hold[_escape] = False
                    elif c == hold[_char]:
                        hold = None
                elif c in holds:
                    hold = [c, False]
            if hold is None:
                line = line.rstrip()
            out.append(line)
        return linebreak.join(out)

    def indebug(self):
        """Checks whether debug mode is active."""
        return self.TRACER.on

    def todebug(self, tag, code):
        """If debugging, prints a debug message."""
        if self.indebug():
            self.TRACER.show("["+str(tag)+"] "+repr(code))

    def pre(self, inputstring, **kwargs):
        """Performs pre-processing."""
        out = str(inputstring)
        for proc in self.preprocs:
            out = proc(out, **kwargs)
            self.todebug(proc.__name__, out)
        return out

    def reind_proc(self, inputstring, strip=True, **kwargs):
        """Reformats indentation."""
        out = inputstring
        if strip:
            out = out.strip()
        out = self.reindent(out)
        if strip:
            out = out.strip()
        out += linebreak
        return out

    def header_proc(self, inputstring, header="file", initial="initial", **kwargs):
        """Adds the header."""
        return headers(initial, self.version) + self.docstring + headers(header, self.version) + inputstring

    def post(self, tokens, **kwargs):
        """Performs post-processing."""
        if len(tokens) == 1:
            out = tokens[0]
            for proc in self.postprocs:
                out = proc(out, **kwargs)
                self.todebug(proc.__name__, out)
            return out
        else:
            raise CoconutException("multiple tokens leftover: "+repr(tokens))

    def autopep8(self, arglist=[]):
        """Enables autopep8 integration."""
        import autopep8
        args = autopep8.parse_args([""]+arglist)
        def pep8_fixer(code, **kwargs):
            """Automatic PEP8 fixer."""
            return autopep8.fix_code(code, options=args)
        self.postprocs.append(pep8_fixer)

    def string_repl(self, tokens):
        """Replaces string references."""
        if len(tokens) == 1:
            ref = self.refs[int(tokens[0])]
            if isinstance(ref, tuple):
                string, strchar, multiline = ref
                if multiline:
                    string = strchar*3+string+strchar*3
                else:
                    string = strchar+string+strchar
                return string
            else:
                raise CoconutException("string marker points to comment/passthrough")
        else:
            raise CoconutException("invalid string marker: "+repr(tokens))

    def set_docstring(self, tokens):
        """Sets the docstring."""
        if len(tokens) == 2:
            self.docstring = self.string_repl([tokens[0]]) + linebreak*2
            return tokens[1]
        else:
            raise CoconutException("invalid docstring tokens: "+repr(tokens))

    def comment_repl(self, tokens):
        """Replaces comment references."""
        if len(tokens) == 1:
            ref = self.refs[int(tokens[0])]
            if isinstance(ref, tuple):
                raise CoconutException("comment marker points to string")
            else:
                return " #"+ref
        else:
            raise CoconutException("invalid comment marker: "+repr(tokens))

    def passthrough_repl(self, tokens):
        """Replaces passthrough references."""
        if len(tokens) == 1:
            ref = self.refs[int(tokens[0])]
            if isinstance(ref, tuple):
                raise CoconutException("passthrough marker points to string")
            else:
                return ref
        else:
            raise CoconutException("invalid passthrough marker: "+repr(tokens))

    def check_strict(self, name, tokens):
        """Checks that syntax meets --strict requirements."""
        if len(tokens) != 1:
            raise CoconutException("invalid "+name+" tokens: "+repr(tokens))
        elif self.strict:
            raise CoconutStyleError("found "+name, tokens[0])
        else:
            return tokens[0]

    def lambdef_check(self, tokens):
        """Checks for Python-style lambdas."""
        return self.check_strict("Python-style lambda", tokens)

    def u_string_check(self, tokens):
        """Checks for Python2-style unicode strings."""
        return self.check_strict("Python-2-style unicode string", tokens)

    def check_py3(self, name, tokens):
        """Checks for Python 3 syntax."""
        if len(tokens) != 1:
            raise CoconutException("invalid "+name+" tokens: "+repr(tokens))
        elif self.version != "3":
            raise CoconutTargetError("found "+name, tokens[0])
        else:
            return tokens[0]

    def typedef_check(self, tokens):
        """Checks for Python 3 type defs."""
        return self.check_py3("Python 3 type def", tokens)

    def yield_from_check(self, tokens):
        """Checks for Python 3 yield from."""
        return self.check_py3("Python 3 yield from", tokens)

    def matrix_at_check(self, tokens):
        """Checks for Python 3.5 matrix multiplication."""
        return self.check_py3("Python 3.5 matrix multiplication", tokens)

    def nonlocal_check(self, tokens):
        """Checks for Python 3 nonlocal statement."""
        return self.check_py3("Python 3 nonlocal statement", tokens)

    def dict_comp_check(self, tokens):
        """Checks for Python 3 dictionary comprehension."""
        return self.check_py3("Python 3 dictionary comprehension", tokens)

    def star_assign_item_check(self, tokens):
        """Checks for Python 3 starred assignment."""
        return self.check_py3("Python 3 starred assignment", tokens)

    def async_stmt_check(self, tokens):
        """Checks for Python 3.5 async statement."""
        return self.check_py3("Python 3.5 async statement", tokens)

    def await_keyword_check(self, tokens):
        """Checks for Python 3.5 await statement."""
        return self.check_py3("Python 3.5 await expression", tokens)

    def complex_raise_stmt_check(self, tokens):
        """Checks for Python 3 raise from statement."""
        return self.check_py3("Python 3 raise from statement", tokens)

    def set_literal_convert(self, tokens):
        """Converts set literals to the right form for the target Python."""
        if len(tokens) != 1:
            raise CoconutException("Invalid set literal tokens: "+repr(tokens))
        elif self.version == "3":
            return "{"+tokens[0]+"}"
        else:
            return "set(["+tokens[0]+"])"

    def parse(self, inputstring, parser, preargs, postargs):
        """Uses the parser to parse the inputstring."""
        try:
            out = self.post(parser.parseString(self.pre(inputstring, **preargs)), **postargs)
        except ParseBaseException as err:
            raise CoconutParseError(err.line, err.col, err.lineno)
        finally:
            self.clean()
        return out

#-----------------------------------------------------------------------------------------------------------------------
# GRAMMAR:
#-----------------------------------------------------------------------------------------------------------------------

    comma = Literal(",")
    dot = ~Literal("..")+Literal(".")
    dubstar = Literal("**")
    star = ~dubstar+Literal("*")
    lparen = Literal("(")
    rparen = Literal(")")
    at = Literal("@")
    arrow = fixto(Literal("->") | Literal("\u2192"), "->")
    dubcolon = Literal("::")
    colon = ~dubcolon+Literal(":")
    semicolon = Literal(";")
    equals = Literal("=")
    lbrack = Literal("[")
    rbrack = Literal("]")
    lbrace = Literal("{")
    rbrace = Literal("}")
    lbanana = Literal("(|")
    rbanana = Literal("|)")
    plus = Literal("+")
    minus = Literal("-")
    bang = fixto(Literal("!") | Literal("\xac"), "!")
    dubslash = Literal("//")
    slash = ~dubslash+Literal("/")
    pipeline = fixto(Literal("|>") | Literal("\u21a6"), "|>")
    starpipe = fixto(Literal("|*>") | Literal("*\u21a6"), "|*>")
    backpipe = fixto(Literal("<|") | Literal("\u21a4"), "<|")
    backstarpipe = fixto(Literal("<*|") | Literal("\u21a4*"), "<*|")
    amp = fixto(Literal("&") | Literal("\u2227") | Literal("\u2229"), "&")
    caret = fixto(Literal("^") | Literal("\u22bb") | Literal("\u2295"), "^")
    bar = fixto(Literal("|") | Literal("\u2228") | Literal("\u222a"), "|")
    percent = Literal("%")
    dotdot = ~Literal("...")+Literal("..")
    dollar = Literal("$")
    ellipses = fixto(Literal("...") | Literal("\u2026"), "...")
    lshift = fixto(Literal("<<") | Literal("\xab"), "<<")
    rshift = fixto(Literal(">>") | Literal("\xbb"), ">>")
    tilde = fixto(Literal("~") | Literal("\xac"), "~")
    underscore = Literal("_")
    pound = Literal("#")
    backtick = Literal("`")
    dubbackslash = Literal("\\\\")
    backslash = ~dubbackslash+Literal("\\")

    lt = ~Literal("<<")+Literal("<")
    gt = ~Literal(">>")+Literal(">")
    eq = Combine(equals + equals)
    le = fixto(Combine(lt + equals) | Literal("\u2264"), "<=")
    ge = fixto(Combine(gt + equals) | Literal("\u2265"), ">=")
    ne = fixto(Combine(bang + equals) | Literal("\u2260"), "!=")

    mul_star = fixto(star | Literal("\u22c5"), "*")
    exp_dubstar = fixto(dubstar | Literal("\u2191"), "**")
    neg_minus = fixto(minus | Literal("\u207b"), "-")
    sub_minus = fixto(minus | Literal("\u2212"), "-")
    div_slash = fixto(slash | Literal("\xf7")+~slash, "/")
    div_dubslash = fixto(dubslash | Combine(Literal("\xf7")+slash), "//")
    matrix_at = at | Literal("\xd7")
    matrix_at_ref = Forward()

    name = Regex("(?![0-9])\\w+")
    for k in keywords + const_vars + reserved_vars:
        name = ~Keyword(k) + name
    for k in reserved_vars:
        name |= fixto(backslash + Keyword(k), k)
    dotted_name = condense(name + ZeroOrMore(dot + name))

    integer = Word(nums)
    binint = Word("01")
    octint = Word("01234567")
    hexint = Word(hexnums)
    anyint = Word(nums, alphanums)

    basenum = Combine(integer + dot + Optional(integer) | Optional(integer) + dot + integer) | integer
    sci_e = CaselessLiteral("e")
    numitem = Combine(basenum + sci_e + integer) | basenum

    number = (attach(Combine(integer + underscore + anyint), anyint_proc)
              | Combine(CaselessLiteral("0b") + binint)
              | Combine(CaselessLiteral("0o") + octint)
              | Combine(CaselessLiteral("0x") + hexint)
              | numitem
              )

    string_ref = Forward()
    moduledoc = Forward()
    comment = Forward()
    passthrough = Forward()
    passthrough_block = Forward()

    string_marker = Combine(Literal('"').suppress() + integer + Literal('"').suppress())
    comment_marker = Combine(pound.suppress() + integer)
    passthrough_marker = Combine(backslash.suppress() + integer)
    passthrough_block_marker = Combine(dubbackslash.suppress() + integer)

    bit_b = Optional(CaselessLiteral("b"))
    raw_r = Optional(CaselessLiteral("r"))
    b_string = Combine((bit_b + raw_r | raw_r + bit_b) + string_ref)
    unicode_u = CaselessLiteral("u").suppress()
    u_string = Combine((unicode_u + raw_r | raw_r + unicode_u) + string_ref)
    u_string_ref = Forward()
    string = b_string | u_string_ref

    lineitem = Combine(Optional(comment) + Literal(linebreak))
    newline = condense(OneOrMore(lineitem))
    startmarker = StringStart() + condense(ZeroOrMore(lineitem) + Optional(moduledoc))
    endmarker = StringEnd()
    indent = Literal(openstr)
    dedent = Literal(closestr)

    augassign = (
        Combine(pipeline + equals)
        | Combine(starpipe + equals)
        | Combine(backpipe + equals)
        | Combine(backstarpipe + equals)
        | Combine(dotdot + equals)
        | Combine(dubcolon + equals)
        | Combine(div_dubslash + equals)
        | Combine(div_slash + equals)
        | Combine(exp_dubstar + equals)
        | Combine(mul_star + equals)
        | Combine(plus + equals)
        | Combine(sub_minus + equals)
        | Combine(percent + equals)
        | Combine(amp + equals)
        | Combine(bar + equals)
        | Combine(caret + equals)
        | Combine(lshift + equals)
        | Combine(rshift + equals)
        | Combine(matrix_at_ref + equals)
        )

    comp_op = (le | ge | ne | lt | gt | eq
               | addspace(Keyword("not") + Keyword("in"))
               | Keyword("in")
               | addspace(Keyword("is") + Keyword("not"))
               | Keyword("is")
               )

    test = Forward()
    expr = Forward()
    comp_for = Forward()

    vardef = name
    typedef = condense(vardef + colon + test)
    typedef_ref = Forward()
    tfpdef = typedef_ref | vardef
    callarg = test
    default = Optional(condense(equals + test))

    argslist = Optional(itemlist(condense(dubstar + tfpdef | star + tfpdef | tfpdef + default), comma))
    varargslist = Optional(itemlist(condense(dubstar + vardef | star + vardef | vardef + default), comma))
    callargslist = Optional(itemlist(condense(dubstar + callarg | star + callarg | callarg + default), comma))

    parameters = condense(lparen + argslist + rparen)

    testlist = itemlist(test, comma)

    dict_comp_ref = Forward()
    yield_from = addspace(Keyword("from") + test)
    yield_from_ref = Forward()
    yield_arg = yield_from_ref | testlist
    yield_expr = addspace(Keyword("yield") + Optional(yield_arg))
    setmaker = addspace(test + comp_for | testlist)
    dict_comp = addspace(condense(test + colon) + test + comp_for)
    dict_item = addspace(itemlist(addspace(condense(test + colon) + test), comma))
    dictmaker = dict_comp_ref | dict_item

    op_atom = condense(
        lparen + (
            fixto(pipeline, "lambda x, f: f(x)")
            | fixto(starpipe, "lambda xs, f: f(*xs)")
            | fixto(backpipe, "lambda f, x: f(x)")
            | fixto(backstarpipe, "lambda f, xs: f(*xs)")
            | fixto(dotdot, "lambda f, g: lambda *args, **kwargs: f(g(*args, **kwargs))")
            | fixto(Keyword("and"), "lambda a, b: a and b")
            | fixto(Keyword("or"), "lambda a, b: a or b")
        ) + rparen | lparen.suppress() + (
            fixto(dot, "__coconut__.getattr")
            | fixto(dubcolon, "__coconut__.itertools.chain")
            | fixto(dollar, "__coconut__.functools.partial")
            | fixto(exp_dubstar, "__coconut__.operator.__pow__")
            | fixto(mul_star, "__coconut__.operator.__mul__")
            | fixto(div_dubslash, "__coconut__.operator.__floordiv__")
            | fixto(div_slash, "__coconut__.operator.__truediv__")
            | fixto(percent, "__coconut__.operator.__mod__")
            | fixto(plus, "__coconut__.operator.__add__")
            | fixto(sub_minus, "__coconut__.operator.__sub__")
            | fixto(neg_minus, "__coconut__.operator.__neg__")
            | fixto(amp, "__coconut__.operator.__and__")
            | fixto(caret, "__coconut__.operator.__xor__")
            | fixto(bar, "__coconut__.operator.__or__")
            | fixto(lshift, "__coconut__.operator.__lshift__")
            | fixto(rshift, "__coconut__.operator.__rshift__")
            | fixto(lt, "__coconut__.operator.__lt__")
            | fixto(gt, "__coconut__.operator.__gt__")
            | fixto(eq, "__coconut__.operator.__eq__")
            | fixto(le, "__coconut__.operator.__le__")
            | fixto(ge, "__coconut__.operator.__ge__")
            | fixto(ne, "__coconut__.operator.__ne__")
            | fixto(tilde, "__coconut__.operator.__inv__")
            | fixto(matrix_at_ref, "__coconut__.operator.__matmul__")
            | fixto(Keyword("not"), "__coconut__.operator.__not__")
            | fixto(Keyword("is"), "__coconut__.operator.is_")
            | fixto(Keyword("in"), "__coconut__.operator.__contains__")
        ) + rparen.suppress()
    )

    testlist_comp = addspace(test + comp_for) | testlist
    func_atom = name | op_atom | condense(lparen + Optional(yield_expr | testlist_comp) + rparen)
    keyword_atom = Keyword(const_vars[0])
    for x in range(1, len(const_vars)):
        keyword_atom |= Keyword(const_vars[x])
    string_atom = addspace(OneOrMore(string))
    passthrough_atom = addspace(OneOrMore(passthrough))
    attr_atom = attach(condense(dot.suppress() + name), attr_proc)
    set_literal_ref = Forward()
    set_s = fixto(CaselessLiteral("s"), "s")
    set_f = fixto(CaselessLiteral("f"), "f")
    set_letter = set_s | set_f
    set_literal = lbrace.suppress() + setmaker + rbrace.suppress()
    set_letter_literal = attach(set_letter + lbrace.suppress() + Optional(setmaker) + rbrace.suppress(), set_proc)
    lazy_items = Optional(test + ZeroOrMore(comma.suppress() + test) + Optional(comma.suppress()))
    lazy_list = attach(lbanana.suppress() + lazy_items + rbanana.suppress(), lazy_list_proc)
    atom = (
        keyword_atom
        | ellipses
        | number
        | string_atom
        | passthrough_atom
        | condense(lbrack + Optional(testlist_comp) + rbrack)
        | condense(lbrace + Optional(dictmaker) + rbrace)
        | set_literal_ref
        | set_letter_literal
        | lazy_list
        | func_atom
        | attr_atom
        )

    slicetest = Optional(test)
    sliceop = condense(colon + slicetest)
    subscript = condense(slicetest + sliceop + Optional(sliceop)) | test
    subscriptlist = itemlist(subscript, comma)
    slicetestgroup = Optional(test, default="")
    sliceopgroup = colon.suppress() + slicetestgroup
    subscriptgroup = Group(slicetestgroup + sliceopgroup + Optional(sliceopgroup) | test)
    simple_trailer = condense(lbrack + subscriptlist + rbrack) | condense(dot + name)
    trailer = (
        Group(condense(dollar + lparen) + callargslist + rparen.suppress())
        | condense(lparen + callargslist + rparen)
        | Group(dotdot + func_atom)
        | Group(condense(dollar + lbrack) + subscriptgroup + rbrack.suppress())
        | Group(condense(dollar + lbrack + rbrack))
        | Group(dollar)
        | simple_trailer
        | Group(condense(lbrack + rbrack))
        | Group(dot)
        )

    assignlist = Forward()
    star_assign_item_ref = Forward()
    simple_assign = condense(name + ZeroOrMore(simple_trailer))
    base_assign_item = condense(simple_assign | lparen + assignlist + rparen | lbrack + assignlist + rbrack)
    star_assign_item = condense(star + base_assign_item)
    assign_item = star_assign_item_ref | base_assign_item
    assignlist <<= itemlist(assign_item, comma)

    atom_item = trace(attach(atom + ZeroOrMore(trailer), item_proc), "atom_item")

    factor = Forward()
    await_keyword_ref = Forward()
    await_keyword = Keyword("await")
    power = trace(condense(addspace(Optional(await_keyword_ref) + atom_item) + Optional(exp_dubstar + factor)), "power")
    unary = plus | neg_minus | tilde

    factor <<= trace(condense(unary + factor) | power, "factor")

    mulop = mul_star | div_dubslash | div_slash | percent | matrix_at_ref
    term = addspace(factor + ZeroOrMore(mulop + factor))
    arith = plus | sub_minus
    arith_expr = addspace(term + ZeroOrMore(arith + term))

    shift = lshift | rshift
    shift_expr = addspace(arith_expr + ZeroOrMore(shift + arith_expr))
    and_expr = addspace(shift_expr + ZeroOrMore(amp + shift_expr))
    xor_expr = addspace(and_expr + ZeroOrMore(caret + and_expr))
    or_expr = addspace(xor_expr + ZeroOrMore(bar + xor_expr))

    chain_expr = attach(or_expr + ZeroOrMore(dubcolon.suppress() + or_expr), chain_proc)

    infix_expr = Forward()
    infix_op = condense(fixto(backtick.suppress(), "(") + chain_expr + fixto(backtick.suppress(), ")"))
    infix_item = attach(Group(Optional(chain_expr)) + infix_op + Group(Optional(infix_expr)), infix_proc)
    infix_expr <<= infix_item | chain_expr

    pipe_op = pipeline | starpipe | backpipe | backstarpipe
    pipe_expr = attach(infix_expr + ZeroOrMore(pipe_op + infix_expr), pipe_proc)

    expr <<= trace(pipe_expr, "expr")
    comparison = addspace(expr + ZeroOrMore(comp_op + expr))
    not_test = addspace(ZeroOrMore(Keyword("not")) + comparison)
    and_test = addspace(not_test + ZeroOrMore(Keyword("and") + not_test))
    or_test = addspace(and_test + ZeroOrMore(Keyword("or") + and_test))
    test_item = or_test
    test_nocond = Forward()
    classic_lambdef_params = parenwrap(lparen, varargslist, rparen)
    new_lambdef_params = lparen.suppress() + varargslist + rparen.suppress()

    classic_lambdef_ref = Forward()
    classic_lambdef = addspace(Keyword("lambda") + condense(classic_lambdef_params + colon) + test)
    new_lambdef = attach(new_lambdef_params + arrow.suppress() + test, lambdef_proc)
    lambdef = trace(classic_lambdef_ref | new_lambdef, "lambdef")

    classic_lambdef_nocond_ref = Forward()
    classic_lambdef_nocond = addspace(Keyword("lambda") + condense(classic_lambdef_params + colon) + test_nocond)
    new_lambdef_nocond = attach(new_lambdef_params + arrow.suppress() + test_nocond, lambdef_proc)
    lambdef_nocond = trace(classic_lambdef_nocond_ref | new_lambdef_nocond, "lambdef_nocond")

    test <<= lambdef | trace(addspace(test_item + Optional(Keyword("if") + test_item + Keyword("else") + test)), "test")
    test_nocond <<= lambdef_nocond | trace(test_item, "test_item")

    simple_stmt = Forward()
    simple_compound_stmt = Forward()
    stmt = Forward()
    suite = Forward()
    nocolon_suite = Forward()

    argument = condense(name + equals + test) | addspace(name + Optional(comp_for))
    classlist = attach(Optional(lparen.suppress() + Optional(testlist) + rparen.suppress()), class_proc)
    classdef = condense(addspace(Keyword("class") + name) + classlist + suite)
    comp_iter = Forward()
    comp_for <<= addspace(Keyword("for") + assignlist + Keyword("in") + test_item + Optional(comp_iter))
    comp_if = addspace(Keyword("if") + test_nocond + Optional(comp_iter))
    comp_iter <<= comp_for | comp_if

    complex_raise_stmt_ref = Forward()
    pass_stmt = Keyword("pass")
    break_stmt = Keyword("break")
    continue_stmt = Keyword("continue")
    return_stmt = addspace(Keyword("return") + Optional(testlist))
    yield_stmt = yield_expr
    simple_raise_stmt = addspace(Keyword("raise") + Optional(test))
    complex_raise_stmt = addspace(simple_raise_stmt + Keyword("from") + test)
    raise_stmt = simple_raise_stmt | complex_raise_stmt_ref
    flow_stmt = break_stmt | continue_stmt | return_stmt | raise_stmt | yield_stmt

    dotted_as_name = addspace(dotted_name + Optional(Keyword("as") + name))
    import_as_name = addspace(name + Optional(Keyword("as") + name))
    import_as_names = itemlist(import_as_name, comma)
    dotted_as_names = itemlist(dotted_as_name, comma)
    import_name = addspace(Keyword("import") + parenwrap(lparen, dotted_as_names, rparen))
    import_from = addspace(Keyword("from") + condense(ZeroOrMore(dot) + dotted_name | OneOrMore(dot))
                   + Keyword("import") + (star | parenwrap(lparen, import_as_names, rparen)))
    import_stmt = import_from | import_name

    namelist = parenwrap(lparen, itemlist(name, comma), rparen)
    global_stmt = addspace(Keyword("global") + namelist)
    nonlocal_stmt = addspace(Keyword("nonlocal") + namelist)
    del_stmt = addspace(Keyword("del") + itemlist(simple_assign, comma))
    with_item = addspace(test + Optional(Keyword("as") + name))

    match = Forward()
    matchlist_list = Group(Optional(match + ZeroOrMore(comma.suppress() + match) + Optional(comma.suppress())))
    matchlist_tuple = Group(Optional(match + OneOrMore(comma.suppress() + match) + Optional(comma.suppress()) | match + comma.suppress()))
    match_const = (
        keyword_atom
        | number
        | string_atom
        | condense(equals.suppress() + simple_assign)
        )
    matchlist_set = Group(Optional(match_const + ZeroOrMore(comma.suppress() + match_const) + Optional(comma.suppress())))
    match_pair = Group(match_const + colon.suppress() + match)
    matchlist_dict = Group(Optional(match_pair + ZeroOrMore(comma.suppress() + match_pair) + Optional(comma.suppress())))
    match_list = lbrack + matchlist_list + rbrack.suppress()
    match_tuple = lparen + matchlist_tuple + rparen.suppress()
    match_lazy = lbanana + matchlist_list + rbanana.suppress()
    base_match = Group(
        match_const("const")
        | (lparen.suppress() + match + rparen.suppress())("paren")
        | (lbrace.suppress() + matchlist_dict + rbrace.suppress())("dict")
        | (Optional(set_s.suppress()) + lbrace.suppress() + matchlist_set + rbrace.suppress())("set")
        | ((match_list | match_tuple | match_lazy) + dubcolon.suppress() + name)("iter")
        | match_lazy("iter")
        | (match_list + plus.suppress() + name + plus.suppress() + match_list)("mseries")
        | (match_tuple + plus.suppress() + name + plus.suppress() + match_tuple)("mseries")
        | ((match_list | match_tuple) + Optional(plus.suppress() + name))("series")
        | (name + plus.suppress() + (match_list | match_tuple))("rseries")
        | (name + equals.suppress() + match)("assign")
        | (name + lparen.suppress() + matchlist_list + rparen.suppress())("data")
        | name("var")
        )
    matchlist_name = name | lparen.suppress() + itemlist(name, comma) + rparen.suppress()
    matchlist_is = base_match + Keyword("is").suppress() + matchlist_name
    is_match = Group(matchlist_is("is")) | base_match
    matchlist_and = is_match + OneOrMore(Keyword("and").suppress() + is_match)
    and_match = Group(matchlist_and("and")) | is_match
    matchlist_or = and_match + OneOrMore(Keyword("or").suppress() + and_match)
    or_match = Group(matchlist_or("or")) | and_match
    match <<= trace(or_match, "match")

    else_suite = condense(suite | colon + trace(attach(simple_compound_stmt, else_proc), "else_suite"))
    else_stmt = condense(Keyword("else") + else_suite)

    match_suite = colon.suppress() + Group((newline.suppress() + indent.suppress() + OneOrMore(stmt) + dedent.suppress()) | simple_stmt)
    full_match = trace(attach(
        Keyword("match").suppress() + match + Keyword("in").suppress() + test + Optional(Keyword("if").suppress() + test) + match_suite
        , match_proc), "full_match")
    match_stmt = condense(full_match + Optional(else_stmt))

    match_assign_stmt = trace(attach(
        (Keyword("match").suppress() | ~(assignlist+equals)) + match + equals.suppress() + (yield_expr | testlist) + newline.suppress()
        , match_assign_proc), "match_assign_stmt")

    case_match = trace(Group(
        Keyword("match").suppress() + match + Optional(Keyword("if").suppress() + test) + match_suite
        ), "case_match")
    case_stmt = attach(
        Keyword("case").suppress() + test + colon.suppress() + newline.suppress()
        + indent.suppress() + Group(OneOrMore(case_match))
        + dedent.suppress() + Optional(Keyword("else").suppress() + else_suite)
        , case_proc)

    assert_stmt = addspace(Keyword("assert") + testlist)
    if_stmt = condense(addspace(Keyword("if") + condense(test + suite))
                       + ZeroOrMore(addspace(Keyword("elif") + condense(test + suite)))
                       + Optional(else_stmt)
                       )
    while_stmt = addspace(Keyword("while") + condense(test + suite + Optional(else_stmt)))
    for_stmt = addspace(Keyword("for") + assignlist + Keyword("in") + condense(testlist + suite + Optional(else_stmt)))
    except_clause = attach(Keyword("except").suppress() + testlist + Optional(Keyword("as").suppress() + name), except_proc)
    try_stmt = condense(Keyword("try") + suite + (
        Keyword("finally") + suite
        | (
            OneOrMore(except_clause + suite) + Optional(Keyword("except") + suite)
            | Keyword("except") + suite
          ) + Optional(else_stmt) + Optional(Keyword("finally") + suite)
        ))
    with_stmt = addspace(Keyword("with") + condense(itemlist(with_item, comma) + suite))

    return_typedef_ref = Forward()
    async_funcdef_ref = Forward()
    async_block_ref = Forward()
    name_funcdef = condense(name + parameters)
    op_funcdef_arg = condense(lparen.suppress() + tfpdef + Optional(default) + rparen.suppress())
    op_funcdef_name = backtick.suppress() + name + backtick.suppress()
    op_funcdef = attach(Group(Optional(op_funcdef_arg)) + op_funcdef_name + Group(Optional(op_funcdef_arg)), op_funcdef_proc)
    return_typedef = addspace(arrow + test)
    base_funcdef = addspace((op_funcdef | name_funcdef) + Optional(return_typedef_ref))
    funcdef = addspace(Keyword("def") + condense(base_funcdef + suite))
    math_funcdef = attach(Keyword("def").suppress() + base_funcdef + equals.suppress() + (yield_expr | testlist), func_proc) + newline
    async_funcdef = addspace(Keyword("async") + (funcdef | math_funcdef))
    async_block = addspace(Keyword("async") + (with_stmt | for_stmt))

    async_match_funcdef_ref = Forward()
    op_match_funcdef_arg = lparen.suppress() + match + rparen.suppress()
    op_match_funcdef = attach(Group(Optional(op_match_funcdef_arg)) + op_funcdef_name + Group(Optional(op_match_funcdef_arg)), op_match_funcdef_proc)
    name_match_funcdef = attach(name + lparen.suppress() + matchlist_list + rparen.suppress(), name_match_funcdef_proc)
    base_match_funcdef = Keyword("def").suppress() + (op_match_funcdef | name_match_funcdef)
    full_match_funcdef = trace(attach(base_match_funcdef + match_suite, full_match_funcdef_proc), "base_match_funcdef")
    math_match_funcdef = attach(
        Optional(Keyword("match").suppress()) + base_match_funcdef + equals.suppress() + (yield_expr | testlist)
        , match_func_proc) + newline
    match_funcdef = Optional(Keyword("match").suppress()) + full_match_funcdef
    async_match_funcdef = addspace(
        (Optional(Keyword("match")).suppress() + Keyword("async") | Keyword("async") + Optional(Keyword("match")).suppress())
        + (full_match_funcdef | math_match_funcdef))
    async_stmt = async_block_ref | async_funcdef_ref | async_match_funcdef

    data_args = Optional(lparen.suppress() + Optional(itemlist(~underscore + name, comma)) + rparen.suppress())
    datadef = condense(attach(Keyword("data").suppress() + name + data_args, data_proc) + suite)

    decorators = attach(OneOrMore(at.suppress() + test + newline.suppress()), decorator_proc)
    decorated = condense(decorators + (
        classdef
        | datadef
        | funcdef
        | match_funcdef
        | async_funcdef_ref
        | async_match_funcdef_ref
        | math_funcdef
        | math_match_funcdef
        ))

    passthrough_stmt = condense(passthrough_block + (nocolon_suite | newline))

    simple_compound_stmt <<= (
        if_stmt
        | try_stmt
        | case_stmt
        | match_stmt
        | passthrough_stmt
        )
    compound_stmt = trace(
        simple_compound_stmt
        | with_stmt
        | while_stmt
        | for_stmt
        | funcdef
        | match_funcdef
        | classdef
        | datadef
        | decorated
        | async_stmt
        | math_funcdef
        | math_match_funcdef
        | match_assign_stmt
        , "compound_stmt")
    expr_stmt = trace(addspace(
                      attach(simple_assign + augassign + (yield_expr | testlist), assign_proc)
                      | ZeroOrMore(assignlist + equals) + (yield_expr | testlist)
                      ), "expr_stmt")

    nonlocal_stmt_ref = Forward()
    keyword_stmt = del_stmt | pass_stmt | flow_stmt | import_stmt | global_stmt | nonlocal_stmt_ref | assert_stmt
    small_stmt = trace(keyword_stmt ^ expr_stmt, "small_stmt")
    simple_stmt <<= trace(condense(itemlist(small_stmt, semicolon) + newline), "simple_stmt")
    stmt <<= trace(compound_stmt | simple_stmt, "stmt")
    nocolon_suite <<= condense(newline + indent + OneOrMore(stmt) + dedent)
    suite <<= trace(condense(colon + nocolon_suite) | addspace(colon + simple_stmt), "suite")
    line = trace(newline | stmt, "line")

    single_input = trace(condense(Optional(line) + ZeroOrMore(newline)), "single_input")
    file_input = trace(condense(ZeroOrMore(line)), "file_input")
    eval_input = trace(condense(testlist + ZeroOrMore(newline)), "eval_input")

    single_parser = condense(startmarker + single_input + endmarker)
    file_parser = condense(startmarker + file_input + endmarker)
    eval_parser = condense(startmarker + eval_input + endmarker)

    def parse_single(self, inputstring):
        """Parses console input."""
        return self.parse(inputstring, self.single_parser, {}, {"header": "none", "initial": "none"})

    def parse_file(self, inputstring):
        """Parses file input."""
        return self.parse(inputstring, self.file_parser, {}, {"header": "file"})

    def parse_exec(self, inputstring):
        """Parses exec input."""
        return self.parse(inputstring, self.file_parser, {}, {"header": "file", "initial": "none"})

    def parse_module(self, inputstring):
        """Parses module input."""
        return self.parse(inputstring, self.file_parser, {}, {"header": "module"})

    def parse_block(self, inputstring):
        """Parses block text."""
        return self.parse(inputstring, self.file_parser, {}, {"header": "none", "initial": "none"})

    def parse_eval(self, inputstring):
        """Parses eval input."""
        return self.parse(inputstring, self.eval_parser, {"strip": True}, {"header": "none", "initial": "none"})

    def parse_debug(self, inputstring):
        """Parses debug input."""
        return self.parse(inputstring, self.file_parser, {"strip": True}, {"header": "none", "initial": "none"})
