"""
handle paths for LIBI77 package (windows)
"""

name = "libI77"


###libI77 is special
###we only need the lib directory. so I won't use the complex search tools


from .envUtils import get_usingLib
from .shutils import env


libI77_lib_envvar = "LIBI77_LIBDIR"

def findLib():
    res = env(libI77_lib_envvar,1)
    if res: return res,get_usingLib("libI77",res,linkas=1)[1]

    import sys, os
    if sys.platform[:6] == 'darwin':
        dirs = ['/sw/lib', '/usr/local/lib', '/usr/lib']# None]
    elif os.name[:5] == "posix":
        dirs = ['/usr/local/lib', '/opt/lib', '/usr/lib']# None]
    else:
        raise Exception("Don't know how to search for library libI77, unknown operating system.")
    
    res,name = get_usingLib("libI77",alt=1,linkas=1)
    if res: return res,name

    for directory in dirs:
        print("Searching %s..." % directory)
        res,name = get_usingLib("libI77",directory,linkas=1)
        if res: return res,name
        continue
        
    #raise EnvironmentError, "Unable to find lib directory of libI77"
    print("Unable to find lib directory of libI77")
    return None,None


libI77_lib,libI77_linkname = findLib()
if not libI77_lib: liblist = []
else: liblist = [libI77_lib]


def find():
    from .Paths import Paths
    paths = Paths( name,
                   description = "I77 lib",
                   origin = 'search libI77 using infect utils',
                   clibs = liblist )
    return paths
