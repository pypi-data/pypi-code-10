
def getEnv( env_variable, default, description = None):
    """return environment variable of env_variable if possible, otherwise
    return default"""
    from os import environ
    try:
        variable = environ[env_variable]
    except KeyError:
        if not default:
            raise RuntimeError('Environment variable %r is not set. The variable should be %r.' % (env_variable, description))
        print("** warning: environment variable %s, which is the %s, is not found. It is set to default value %s" % (env_variable, description, default))
        variable = default
    return variable

from .shutils import *
from ._utils import *
from os import environ

def set_environ(name,value):
    '''set_environ(name,value) --> setenv a value'''
    os.environ[name] = value
    return


def get_execPath(name,allowlink=False):
    '''get_execPath(name,[allowlink]) --> use which; defaults to link root'''
    DIR = which(name,allowlink)
    if not DIR:
        raise EnvironmentError("unable to find %r" % name)
    return DIR


def get_usingExec(binName,split=None):
    '''get_usingExec(binName,[split]) --> getenv keyed on binName'''
    if not split: split = 'bin'
    DIR = get_execPath(binName)
    DIR = split.join(DIR.split(split)[:-1])
    return DIR


def set_usingExec(envName,binName,split=None):
    '''set_usingExec(envName,binName,[split]) --> setenv keyed on binName'''
    DIR = get_usingExec(binName, split)
    set_environ(envName,DIR)
    return


def get_usingLib(libName,root=None,alt=0,linkas=0):
    '''get_usingLib(libName,[root,alt,linkas]) --> getenv keyed on libName'''
    #if root == None:  root = getROOT()
    #if libName: libName = '*'+libName+'*'
    if not alt:
        if root == None: root = getROOT()
        if libName: libName = '*'+libName+'*'
        LIB_LIST = find(libName,root,type='f')
        LIB = prunelist(LIB_LIST,all=False)
    else:
        if libName: libName = 'lib'+libName
        try: LIB = whereis(libName)
        except:
            if linkas: return None,None
            return None #system does not have 'whereis' command
    print("found %s" % LIB)
    #if files found do not end with correct extension, discard the file
    if not (LIB.endswith(".so") or LIB.endswith(".a") or LIB.endswith(".dylib") or LIB.find(".so.")!=-1 or LIB.endswith(".lib") ):
        print("but %s is not a library" % LIB)
        if linkas: return None,None
        return None
    sep = getSEP()
    LIBbits = LIB.split(sep)
    LIBNAME = LIBbits.pop()
    LIBNAME = LIBNAME.split('.')[0]
    from sys import platform
    if platform[:3] != 'win':
        LIBNAME = LIBNAME[3:]
    LIBDIR = sep.join(LIBbits)
    if not linkas: return LIBDIR
    return LIBDIR, LIBNAME


def set_usingLib(envName,libName,root=None):
    '''set_usingLib(envName,binName,[root]) --> setenv keyed on libName'''
    DIR = get_usingLib(libName, root)
    set_environ(envName,DIR)
    return

if __name__=='__main__':
    import sys
    try:
        func = sys.argv[1]
    except: func = None
    if func:
        try:
            exec('print %s' % func)
        except:
            print("Error: incorrect syntax '%s'" % func)
            exec('print %s.__doc__' % func.split('(')[0])
    else: pass

