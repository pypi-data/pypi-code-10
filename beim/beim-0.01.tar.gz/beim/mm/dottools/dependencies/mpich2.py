#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

def render( paths ):
    root = paths.root
    ver = getVersion(paths)
    lines = [
        "export MPI_DIR='%s'" % root,
        "export MPI_INCDIR='%s'" % paths.includes[0],
        "export MPI_LIBDIR='%s'" % paths.clibs[0],
        "export MPI_VERSION=mpich2-%s" % ver,
        #"export MPI_INCLUDES='%s'" % ':'.join(paths.includes),
        #"export MPI_LIBS='%s'" % ':'.join(paths.clibs),
        ]
    return lines


def getVersion(paths):
    # assumption: mpich2version is under $root/bin
    import os
    exe = os.path.join(paths.root, 'bin', 'mpich2version')
    if not os.path.exists(exe):
        raise RuntimeError("%s does not exist" % exe)
    import subprocess
    p = subprocess.Popen(exe, stdout=subprocess.PIPE)
    if p.wait():
        raise RuntimeError("%s failed" % exe)
    out, e = p.communicate()
    line1 = out.splitlines()[0]
    tokens = line1.split()
    return tokens[-1]
    
        

# version
__id__ = "$Id$"

# End of file 
