"""
handle paths for HDF4 package
"""

name = 'HDF4'
description = 'NCSA Hierarchiacal Data Format version 4'

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


fromEnvVars = PathsFinder( name, description, hints = "HDF4" )


from .FromExecutable import PathsFinder
fromExe = PathsFinder( name, description, hints = {"executable": "h4cc"} )

toolset  = [fromEnvVars,
            fromExe,]


def find():
    from .search import search
    paths = search(toolset)
    return paths
