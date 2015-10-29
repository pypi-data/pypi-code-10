"""
handle paths for matlab package
"""

name = "Matlab"
description = 'Mathworks Matlab'


Matlab_scheme = {
    'root': '.',
    'c headers': 'extern/include',
    'c libraries': None,
    'python modules': 'do_python_modules_exist?'}


from .FromEnvVariables import PathsFinder as base_FromEnvVars
class FromEnvVars(base_FromEnvVars):
    scheme = Matlab_scheme
    pass
fromEnvVars = FromEnvVars( name, description, hints = "MATLAB" )
    

from .FromExecutable import PathsFinder as base_FromExe
class FromExe(base_FromExe):
    scheme = Matlab_scheme
    pass
exe_hints = {"executable": "matlab", "c libraries": "bin/*"}
#Matlab6    {"executable": "matlab", "c libraries": "extern/lib/*"}
fromExe = FromExe( name, description, hints = exe_hints )


def find():
    from .search import search
    toolset  = [fromEnvVars, fromExe,]
    paths = search(toolset)
    return paths
