"""
handle paths for db2latex xsl
"""

name = 'db2latex'
description = 'docbook->latex xsl'

from .FromEnvVariables import PathsFinder

fromEnvVars = PathsFinder( name, description, hints = "DB2LATEX_XSL" )

toolset  = [fromEnvVars,]


def find():
    from .search import search
    paths = search(toolset)
    return paths
