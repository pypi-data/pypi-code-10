"""
handle paths for mpich2 package
"""

name = 'mpich2'
description = 'Argonne MPI implementation'


def validate(paths):
    import os
    from .PathsFinder import assertExists
    assertExists('mpi.h', paths.includes)
    assertExists('libmpich.so*', paths.clibs)
    return


from .FromDefaultLocations import PathsFinder as _DefLocBase
class PathsFinder(_DefLocBase):
    import os
    if os.uname()[3].find('Ubuntu') != 0:
        scheme = {'root': '.',
                  'c headers': 'include/mpich2',
                  'c libraries': 'lib',
                  'python modules': 'unknown'}
    
fromDefaultLoc = PathsFinder(name, description, validator=validate)


from .FromEnvVariables import PathsFinder as _EnvPFBase
class PathsFinder(_EnvPFBase):
    import os
    if os.name == "nt":
        scheme = {'root': '.',
                  'c headers': 'include',
                  'c libraries': 'dll',
                  'python modules': 'python'}
        pass

    pass # end of PathsFinder


fromEnvVars = PathsFinder( name, description, hints = "MPI",
                           validator=validate)


from .FromExecutable import PathsFinder
fromExe = PathsFinder( name, description, hints = {"executable": "mpicxx"},
                       validator = validate)

toolset  = [fromDefaultLoc,
            fromEnvVars,
            fromExe,]


def find():
    from .search import search
    paths = search(toolset)
    return paths
