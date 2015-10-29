"""
handle paths for h4h5tools package
"""

name = 'h4h5tools'
description = 'NCSA Hierarchiacal Data Format (HDF) conversion tools for version 4<->5'

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


fromEnvVars = PathsFinder( name, description, hints = "H4H5TOOLS" )


from .FromExecutable import PathsFinder
fromExe = PathsFinder( name, description, hints = {"executable": "h4toh5"} )

toolset  = [fromEnvVars,
            fromExe,]


def find():
    from .search import search
    paths = search(toolset)
    return paths

