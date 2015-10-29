#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010 All Rights Reserved 
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def checkout( package, dest, dry_run=0 ):
    """check out a package at "dest" directory"""
    name = package.name
    print('* Working on %s' % name)
    cmd = "cd %s; " % dest
    cocmd = package.repo.checkout_command
    if cocmd:
        cmd += cocmd
        print(cmd)
        if not dry_run:
            if os.system(cmd): print("Unable to check out %s" % name)
        pass
    if not dry_run:
        patch(package, dest)
    return


def update( package, dest, dry_run=0 ):
    """update a package at "dest" directory"""
    name = package.name
    print('* Working on %s' % name)
    path = name
    p = os.path.join( dest, path )
    cmd = "cd %s; " % p
    udcmd = package.repo.update_command
    if udcmd:
        cmd += udcmd
        print(cmd)
        if not dry_run:
            if os.system(cmd): print("Unable to update %s" % name)
        pass
    if not dry_run:
        patch(package, dest)
    return


def patch( package, dest):
    patch = getattr(package, 'patch', None)
    name = package.name
    if not patch: 
        print("No patch for package %s" % name)
        return

    print('patching %s ...' % name)
    path = name
    dest = os.path.join( dest, path )
    patch(dest)
    print('done')
    return


import os

# version
__id__ = "$Id$"

# End of file 
