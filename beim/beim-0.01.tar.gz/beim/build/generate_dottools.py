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

# make-dottools.py <directory>


def render( path, export_root, build_root, merlin_dir):
    import os
    
    from deps import packages
    dependencies = ['Python'] + packages

    dottoolspath = os.path.join( path, 'dottools' )
    customization_path = os.path.join( path, 'dottools.customized' )
    from ..mm.dottools_factory import render_file
    render_file(
        dottoolspath, dependencies,
        export_root, build_root, merlin_dir,
        customization_path = customization_path,
        )
    return dottoolspath


from ..mm.dottools_factory import DependencyMissing


# version
__id__ = "$Id$"

# End of file 


