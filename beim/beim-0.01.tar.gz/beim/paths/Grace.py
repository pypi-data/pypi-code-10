"""
handle paths for grace package
"""

name = 'grace'
description = 'grace WYSIWYG 2-D plotting package'               


from .FromEnvVariables import PathsFinder 
fromEnvVars = PathsFinder( name, description, hints = "GRACE" )


from .FromExecutable import PathsFinder
fromExe = PathsFinder( name, description, hints = {"executable": "grace"} )

toolset  = [fromEnvVars,
            fromExe,]


def find():
    from .search import search
    paths = search(toolset)
    return paths
