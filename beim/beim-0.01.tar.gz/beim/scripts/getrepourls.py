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


def main():
    import packages
    from ..packages.factories import fromPyPackage
    pkgcontainer = fromPyPackage.factory(packages)
    packages = pkgcontainer.getAll()

    from ..packages import getRepoUrls
    urls = getRepoUrls(packages)
    printUrls(urls)
    return


def printUrls(urls):
    import sys
    argv = sys.argv
    if len(argv) == 2:
        type = argv[1]
    else:
        type = None
    
    if type == 'pylist':
        print('[')
        for url in urls: 
            print('%r' % url, ',')
            continue
        print(']')
    else:
        for url in urls: print(url)
    return


# version
__id__ = "$Id: getrepourls.py 530 2010-11-05 23:42:38Z linjiao $"

# End of file 
