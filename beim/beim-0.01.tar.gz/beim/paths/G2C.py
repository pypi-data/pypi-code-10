"""
handle paths for G2C package
"""

name = "g2c"


###g2c is special
###we only need the lib directory. so I won't use the complex search tools


from .envUtils import get_usingLib
from .shutils import env


g2c_lib_envvar = "G2C_LIBDIR"

def findLib():
    res = env(g2c_lib_envvar,1)
    if res: return res,get_usingLib("g2c",res,linkas=1)[1]

    import sys, os
    if sys.platform[:6] == 'darwin':
        dirs = ['/sw/lib', '/usr/local/lib', '/usr/lib']# None]
    elif os.name[:5] == "posix":
        dirs = ['/usr/local/lib', '/opt/lib', '/usr/lib']# None]
    else:
        raise Exception("Don't know how to search for library g2c, unknown operating system.")
    
    res,name = get_usingLib("g2c",alt=1,linkas=1)
    if res: return res,name
    
    for directory in dirs:
        print("Searching %s..." % directory)
        res,name = get_usingLib("g2c",directory,linkas=1)
        if res: return res,name
        continue
        
    #raise EnvironmentError, "Unable to find lib directory of g2c"
    print("Unable to find lib directory of g2c")
    return None,None



def find():
    g2c_lib,g2c_linkname = findLib()
    if not g2c_lib: liblist = []
    else: liblist = [g2c_lib]


    from .Paths import Paths
    paths = Paths( name,
                   description = "Linear Algebra PACKage",
                   origin = 'search libg2c.so using infect utils',
                   clibs = liblist )
    return paths
