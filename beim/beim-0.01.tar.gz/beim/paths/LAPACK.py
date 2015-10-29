"""
handle paths for LAPACK package
"""

name = "lapack"


###lapack is special
###we only need the lib directory. so I won't use the complex search tools


from .envUtils import get_usingLib
from .shutils import env


lapack_lib_envvar = "LAPACK_LIBDIR"

def findLib():
    res = env(lapack_lib_envvar,1)
    if res: return res,get_usingLib("lapack",res,linkas=1)[1]

    import sys, os
    if sys.platform[:6] == 'darwin':
        dirs = ['/sw/lib', '/usr/local/lib', '/usr/lib']# None]
    elif os.name[:5] == "posix":
        dirs = ['/usr/local/lib', '/opt/lib', '/usr/lib']# None]
    else:
        raise InstallationNotFound("Don't know how to search for library lapack, unknown operating system.")
    
    res,name = get_usingLib("lapack",alt=1,linkas=1)
    if res: return res,name

    for directory in dirs:
        print("Searching %s..." % directory)
        res,name = get_usingLib("lapack",directory,linkas=1)
        if res: return res,name
        continue
        
    #raise EnvironmentError, "Unable to find lib directory of lapack"
    print("Unable to find lib directory of lapack")
    return None,None


from .InstallationNotFound import InstallationNotFound

lapack_lib,lapack_linkname = findLib()
if not lapack_lib:
    raise InstallationNotFound("lapack")
else: liblist = [lapack_lib]


def find():
    from .Paths import Paths
    paths = Paths( name,
                   description = "Linear Algebra PACKage",
                   origin = 'search liblapack.so using infect utils',
                   clibs = liblist )
    return paths
