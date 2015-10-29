"""
handle paths for HDF5 package
"""

from .InstallationNotFound import InstallationNotFound

name = 'HDF5'
description = 'NCSA Hierarchiacal Data Format'

# validator 
# search all include dirs to find hdf5.h
def validator(paths):
    import os
    found = False
    for directory in paths.includes:
        candidate = os.path.join(directory,'hdf5.h')
        print("* Looking for %s" % candidate)
        if os.path.exists(candidate): found=True; break
        print("... not found")
        continue
    if not found: 
        raise RuntimeError("Cannot find hdf5.h in candidate %s" % paths)
    return



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
fromEnvVars = PathsFinder( name, description, hints = "HDF5", validator=validator) 


from .FromExecutable import PathsFinder
fromExe = PathsFinder( name, description, hints = {"executable": "h5cc"}, validator=validator)

toolset  = [fromEnvVars,
            fromExe,]


def find():
    from .search import search
    paths = search(toolset)
    return paths
