
import pkgutil
import sys
import imp
import os

def macroCommand(macroCmdLine):
    if len(macroCmdLine) > 0 and macroCmdLine[0] == '%':
        retval = runMacro(macroCmdLine)
        if retval != None:
            print retval
        return True

    return False

def runMacro(macroCmdLine):

    try:

        vars = macroCmdLine.split()

        if  vars[0][0] != '%':
            raise MacroError(r"macro name must begin with %")

        macro = getMacro( vars[0][1:] )

        vars = vars[1:]

        ret = macro( *vars )

        if not ret:
            ret = ''

        return ret

    except MacroError:
        sys.stderr.write( "MACRO ERROR: %s\n" % sys.exc_info()[1] )

class MacroError(Exception):

    def __init__(self, desc):
        self.desc = desc

    def __str__(self):
        return self.desc

def registerMacros():

    import karmadbg.macros

    for loader, module_name, ispkg in pkgutil.iter_modules( karmadbg.macros.__path__):
        if not ispkg:
            loader.find_module(module_name).load_module(module_name)

def registerMacro(fn, name = "", desc = ""):

    if not name:
        name = fn.func_name
    if not desc:
        if fn.__doc__:
            desc = fn.__doc__
        else:
            desc = "\n" +  name + "\n"

    macroList[name]= (fn, desc)

def getMacro(macroName):
    try:
        global macroList
        return macroList[macroName][0]
    except KeyError:
        raise MacroError("macro \'%s\' is not found\n" % macroName)

def getMacroDesc(macroName):
    try:
        global macroList
        return macroList[macroName][1]
    except KeyError:
        raise MacroError("macro \'%s\' is not found\n" % macroName)

def macrocmd(*args, **kwargs):

    name = ''
    desc = ''

    def decorator(macrofn):
        registerMacro(macrofn, name=name, desc=desc)

    if len(args) == 1 and callable(args[0]):
        registerMacro(args[0])
        return args[0]

    if 'name' in kwargs:
        name = kwargs['name']
    if 'desc' in kwargs:
        desc = kwrags['desc']

    return decorator


macroList = {}
