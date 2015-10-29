"""
handle paths for danse_texcommon package
"""

name = 'danse_texcommon'
description = 'tex style files for danse'

from .FromEnvVariables import PathsFinder

fromEnvVars = PathsFinder( name, description, hints = "DANSE_TEXCOMMON" )

toolset  = [fromEnvVars,]

def find():
    from .search import search
    paths = search(toolset)
    return paths
