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

# script to build envs.sh


PYTHON_SUBDIR = 'packages'


def createEnvVarOps(package, export):
    import os
    from ..envvars.operations import Set, Prepend
    ops = []
    
    ops.append(Set('PYRE_DIR', export))
    ops.append(Set('%s_DIR' % package.upper(), export))
    
    depsbin = os.path.join(export, 'deps', 'bin')
    ops.append(Prepend('PATH', depsbin))
    
    bin = os.path.join(export, 'bin')
    ops.append(Prepend('PATH', bin))
    
    depslib = os.path.join(export, 'deps', 'lib')
    ops.append(Prepend('LD_LIBRARY_PATH', depslib))
    ops.append(Prepend('DYLD_LIBRARY_PATH', depslib))

    lib = os.path.join(export, 'lib')
    ops.append(Prepend('LD_LIBRARY_PATH', lib))
    ops.append(Prepend('DYLD_LIBRARY_PATH', lib))

    depspy = os.path.join(export, 'deps', 'python')
    ops.append(Prepend('PYTHONPATH', depspy))
    
    py = os.path.join(export, PYTHON_SUBDIR)
    ops.append(Prepend('PYTHONPATH', py))

    return ops


def build_envs_sh(package, target, envvarops_factory=None):
    """build envs.sh on target's bin directory
    
    package: name of the package, eg luban
    target: path at which the package was installed. for mm user, this is EXPORT_ROOT
    """
    import os
    target = os.path.abspath( target )
    print('building envs.sh for %s' % target)

    # content of the envs.sh
    opsfactory = envvarops_factory or createEnvVarOps
    ops = opsfactory(package, target)
    from ..envvars.renderers.BashScriptor import BashScriptor
    scriptor = BashScriptor()
    lines = scriptor.render(ops)
    content = '\n'.join(lines)
    
    # 
    bindir = os.path.join( target, 'bin' )
    # make dir if necessary
    if not os.path.exists(bindir): os.makedirs(bindir)
    
    # envs.sh
    f = os.path.join( bindir, 'envs.sh' )
    open(f, 'w').write(content)
    return


def createMain(package, template=None, envvarops_factory=None):
    "factory to create 'main' function"
    if template:
        from ._build_envs_usingtemplate import createMain
        return createMain(package, template=template)
    
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

        build_envs_sh(package, path, envvarops_factory = envvarops_factory)
        return
    return main


# version
__id__ = "$Id$"

# End of file 
