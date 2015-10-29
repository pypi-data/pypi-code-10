"""
handle paths for ATLAS package
"""

name = "atlas"


###atlas is special
###we only need the lib directory. so I won't use the complex search tools


from .envUtils import get_usingLib
from .shutils import env


atlas_lib_envvar = "ATLAS_LIBDIR"

def findLib():
    res = env(atlas_lib_envvar,1)
    if res: return res,get_usingLib("atlas",res,linkas=1)[1]

    import sys, os
    if sys.platform[:6] == 'darwin':
        dirs = ['/sw/lib', '/usr/local/lib', '/usr/lib']# None]
    elif os.name[:5] == "posix":
        dirs = ['/usr/local/lib', '/opt/lib', '/usr/lib']# None]
    else:
        raise InstallationNotFound("Don't know how to search for library atlas, unknown operating system.")
    
    res,name = get_usingLib("atlas",alt=1,linkas=1)
    if res: return res,name
    
    for directory in dirs:
        print("Searching %s..." % directory)
        res,name = get_usingLib("atlas", directory,linkas=1)
        if res: return res,name
        continue
        
    #raise EnvironmentError, "Unable to find lib directory of atlas"
    print("Unable to find lib directory of atlas")
    return None,None


from .InstallationNotFound import InstallationNotFound


atlas_lib,atlas_linkname = findLib()
if not atlas_lib:
    raise InstallationNotFound("atlas")
else: liblist = [atlas_lib]


def find():
    from .Paths import Paths
    paths = Paths( name,
                   description = "Linear Algebra PACKage",
                   origin = 'search libatlas.so using infect utils',
                   clibs = liblist )
    return paths
