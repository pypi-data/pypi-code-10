"""
handle paths for BLAS package
"""

name = "blas"


###blas is special
###we only need the lib directory. so I won't use the complex search tools


from .envUtils import get_usingLib
from .shutils import env


blas_lib_envvar = "BLAS_LIBDIR"

def findLib():
    res = env(blas_lib_envvar,1)
    if res: return res,get_usingLib("blas",res,linkas=1)[1]

    import sys, os
    if sys.platform[:6] == 'darwin':
        dirs = ['/sw/lib', '/usr/local/lib', '/usr/lib']# None]
    elif os.name[:5] == "posix":
        dirs = ['/usr/local/lib', '/opt/lib', '/usr/lib']# None]
    else:
        raise InstallationNotFound("Don't know how to search for library blas, unknown operating system.")
    
    res,name = get_usingLib("blas",alt=1,linkas=1)
    if res: return res,name

    for directory in dirs:
        print("Searching %s..." % directory)
        res,name = get_usingLib("blas",directory,linkas=1)
        if res: return res,name
        continue
        
    #raise EnvironmentError, "Unable to find lib directory of blas"
    print("Unable to find lib directory of blas")
    return None,None


from .InstallationNotFound import InstallationNotFound

blas_lib,blas_linkname = findLib()
if not blas_lib:
    raise InstallationNotFound("blas")
else: liblist = [blas_lib]



def find():
    from .Paths import Paths
    paths = Paths( name,
                   description = "Linear Algebra PACKage",
                   origin = 'search libblas.so using infect utils',
                   clibs = liblist )
    
