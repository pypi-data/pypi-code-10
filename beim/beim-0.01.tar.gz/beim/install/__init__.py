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


def copy_all( src, target, **opts ):
    "copy everything under src to target"
    from distutils.dir_util import copy_tree
    copy_tree( src, target, **opts )
    return



fmtstr = """
root=%s
deps=$root/deps

export PYRE_DIR=$root
export PATH=$root/bin:$deps/bin:$PATH
export LD_LIBRARY_PATH=$root/lib:$deps/lib:$LD_LIBRARY_PATH
export DYLD_LIBRARY_PATH=$root/lib:$deps/lib:$DYLD_LIBRARY_PATH
export PYTHONPATH=$root/modules:$deps/python:$PYTHONPATH
"""

def envs_sh_content(root):
    return fmtstr % root

def build_envs_sh( target, content=None ):
    "build envs.sh on target's bin directory"
    import warnings
    warnings.warn('beim.install.build_envs_sh is obsolete. use beim.scripts.build_envs_sh')
    
    import os
    target = os.path.abspath( target )

    # content of the envs.sh
    if content is None: content = envs_sh_content(target)
    
    # 
    bindir = os.path.join( target, 'bin' )
    # make dir if necessary
    if not os.path.exists(bindir): os.makedirs(bindir)
    
    # envs.sh
    f = os.path.join( bindir, 'envs.sh' )
    open(f, 'w').write(content)
    
    return
    

# version
__id__ = "$Id$"

# End of file 
