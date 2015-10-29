"""
handle paths for gcc package
"""

name = 'gcc'
description = 'gcc compiler'


def validate(paths):
    import os
    from .PathsFinder import assertExists
    # assertExists('???.h', paths.includes)
    return


from .FromExecutable import PathsFinder
fromExe = PathsFinder( 
    name, description, 
    hints = {"executable": "gcc"},
    validator = validate)

toolset  = [fromExe,]


def find():
    from .search import search
    paths = search(toolset)
    return paths
