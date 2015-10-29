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


def getRepoUrls(packages):
    return [p.repo.url for p in packages]


def checkout( packages, dest, dry_run=0 ):
    """check out packages at "dest" directory"""
    from beim.package import checkout
    for package in packages:
        checkout(package, dest, dry_run=dry_run)
        continue
    return


def update( packages, dest, dry_run=0 ):
    """update packages at "dest" directory"""
    from beim.package import update
    for package in packages:
        update(package, dest, dry_run=dry_run)
        continue
    return


# version
__id__ = "$Id$"

# End of file 
