"""
handle paths for idl package
"""

name = "IDL"
description = 'rsi IDL'

import os

IDL_scheme = {
    'root': '.',
    'c headers': os.path.join('external','include'),
    'c libraries': None,
    'python modules': 'do_python_modules_exist?'}

IDL_env_var_scheme = {
    'root': '_DIR',
    'c headers': '_INCDIR',
    'c libraries': '_BINDIR',
    'python modules': 'do_python_modules_exist'}



from .FromEnvVariables import PathsFinder as base_FromEnvVars
class FromEnvVars(base_FromEnvVars):
    scheme = IDL_scheme
    env_var_scheme = IDL_env_var_scheme
    pass
fromEnvVars = FromEnvVars( name, description, hints = "IDL" )



from .FromExecutable import PathsFinder as base_FromExe
class FromExe(base_FromExe):
    scheme = IDL_scheme
    pass

from sys import platform
if platform[:3] == 'win':
    IDLEXE = "idlde.exe"
else:
    IDLEXE = "idl"
    
fromExe = FromExe( name, description,
                   hints = {"executable": IDLEXE,
                            "c libraries": "bin/bin*",
                            "c headers": "external/include"} )

toolset  = [fromEnvVars, fromExe,]


def find():
    from .search import search
    paths = search(toolset)
    return paths


