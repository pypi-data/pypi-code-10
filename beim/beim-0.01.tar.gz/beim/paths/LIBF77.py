"""
handle paths for LIBF77 package (windows)
"""

name = "libF77"


###libF77 is special
###we only need the lib directory. so I won't use the complex search tools


from .envUtils import get_usingLib
from .shutils import env


libF77_lib_envvar = "LIBF77_LIBDIR"

def findLib():
    res = env(libF77_lib_envvar,1)
    if res: return res,get_usingLib("libF77",res,linkas=1)[1]

    import sys, os
    if sys.platform[:6] == 'darwin':
        dirs = ['/sw/lib', '/usr/local/lib', '/usr/lib']# None]
    elif os.name[:5] == "posix":
        dirs = ['/usr/local/lib', '/opt/lib', '/usr/lib']# None]
    else:
        raise InstallationNotFound("Don't know how to search for library libF77, unknown operating system.")
    
    res,name = get_usingLib("libF77",alt=1,linkas=1)
    if res: return res,name

    for directory in dirs:
        print("Searching %s..." % directory)
        res,name = get_usingLib("libF77",directory,linkas=1)
        if res: return res,name
        continue
        
    #raise EnvironmentError, "Unable to find lib directory of libF77"
    print("Unable to find lib directory of libF77")
    return None,None


from .InstallationNotFound import InstallationNotFound

libF77_lib,libF77_linkname = findLib()
if not libF77_lib:
    raise InstallationNotFound("libf77")
else: liblist = [libF77_lib]


def find():
    from .Paths import Paths
    paths = Paths( name,
                   description = "F77 lib",
                   origin = 'search libF77 using infect utils',
                   clibs = liblist )
    return paths
