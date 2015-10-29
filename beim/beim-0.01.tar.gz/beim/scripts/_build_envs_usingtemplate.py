#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

import warnings
warnings.warn('This is obsolete. Consider rewrite using beim.envvars.operations.')

# script to build envs.sh


fmtstr = """
export_root=%(export_root)s
deps=$export_root/deps

export %(package)s_DIR=$export_root
export PYRE_DIR=$export_root
export PATH=$export_root/bin:$deps/bin:$PATH
export LD_LIBRARY_PATH=$export_root/lib:$deps/lib:$LD_LIBRARY_PATH
export DYLD_LIBRARY_PATH=$export_root/lib:$deps/lib:$DYLD_LIBRARY_PATH
export PYTHONPATH=$export_root/modules:$deps/python:$PYTHONPATH
"""

def envs_sh_content(root, package, template=None):
    if template is None: template = fmtstr
    return template % {'export_root': root, 'package': package.upper()}


def build_envs_sh( package, target, content=None, template=None):
    """build envs.sh on target's bin directory
    
    package: name of the package, eg luban
    target: path at which the package was installed. for mm user, this is EXPORT_ROOT
    """
    import os
    target = os.path.abspath( target )
    print('building envs.sh for %s' % target)

    # content of the envs.sh
    if content is None: 
        content = envs_sh_content(target, package, template=template)
    
    # 
    bindir = os.path.join( target, 'bin' )
    # make dir if necessary
    if not os.path.exists(bindir): os.makedirs(bindir)
    
    # envs.sh
    f = os.path.join( bindir, 'envs.sh' )
    open(f, 'w').write(content)
    return


def createMain(package, template=None):
    "factory to create 'main' function"
    def main():
        usage = 'usage: %prog ' + 'path-to-%s-installation' % package

        import optparse
        parser = optparse.OptionParser(usage=usage)

        options, args = parser.parse_args()

        if len(args) > 1:
            parser.print_usage()
            return

        if len(args) == 0:
            from beim.datastore import open
            build_info = open('build_info')
            path = build_info.get('export_root', 'EXPORT')
        else:
            path = args[0]

        build_envs_sh(package, path, template=template)
        return
    return main


# version
__id__ = "$Id$"

# End of file 
