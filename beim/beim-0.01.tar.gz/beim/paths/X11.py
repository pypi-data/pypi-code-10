"""
handle paths for x11 package
"""

name = "X11"
description = "X11"


from .FromEnvVariables import PathsFinder 
fromEnvVars = PathsFinder(name, description, hints = "X11")

from .FromExecutable import PathsFinder 
fromExe = PathsFinder(name, description, hints = {"executable":"startx"} )


def find():
    from .search import search
    toolset  = [fromEnvVars, fromExe,]
    paths = search(toolset)
    return paths
