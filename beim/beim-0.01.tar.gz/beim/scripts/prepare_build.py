#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2007-2010 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def prepare_build(export_root):
    import sys, os
    pwd = os.path.abspath( os.curdir )

    import sys
    sys.path = [pwd] + sys.path

    from beim.build import prepare_build
    prepare_build( pwd, export_root=export_root)
    return


def getsrc():
    # getsrc if necessary
    p = 'src'
    if hasSubdirs(p): return
    from .getsrc import main
    main()
    return


def hasSubdirs(p):
    skip = '.svn'
    import os
    entries = os.listdir(p)
    for e in entries:
        if e in skip: continue
        p1 = os.path.join(p, e)
        if os.path.isdir(p1): return True
        continue
    return False


def main():
    getsrc()
    import sys, os, shlex

    # find out the "export" directory that user wants
    from beim.datastore import open
    build_info = open('build_info')
    
    if len(sys.argv) == 2:
        export_root = sys.argv[1]
    else:
        if build_info.get('export_root'):
            export_root = build_info['export_root']
        else:
            export_root = os.path.abspath('EXPORT')

    build_info['export_root'] = export_root
    del build_info

    # adjust env vars so that <export>/deps is in use
    deps_root = os.path.join(export_root, 'deps')
    env = os.environ.copy()
    env['PATH'] = '%s:%s' % (
        os.path.join( deps_root, 'bin' ), env['PATH'] )
    env['LD_LIBRARY_PATH'] = '%s:%s' % (
        os.path.join( deps_root, 'lib' ), env.get('LD_LIBRARY_PATH') or '' )
    env['DYLD_LIBRARY_PATH'] = '%s:%s' % (
        os.path.join( deps_root, 'lib' ), env.get('DYLD_LIBRARY_PATH') or '' )
    env['PYTHONPATH'] = '%s:%s' % (
        os.path.join( deps_root, 'python' ), env.get('PYTHONPATH', '') )

    # open a sub process to run the build
    cmd = '%s -c "from beim.scripts.prepare_build import prepare_build; prepare_build(%r)"' % (
        sys.executable, export_root)
    args = shlex.split(cmd)

    import subprocess
    p = subprocess.Popen(args, env=env)
    while 1:
        p.communicate()
        rt = p.poll()
        if rt is not None: break
        continue
    if rt:
        raise RuntimeError("Command %s failed or aborted" % cmd)
    

# version
__id__ = "$Id$"

# End of file 
