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

"""
create a "packages" container from a python subpackage.
The python subpackage must contain a bunch of modules,
each of which describes a package.

In detail, we need:

bundles.py: packages are grouped into bundles. change it when new packages
            are added or when bundles need to be restructured
defaults.py: default packages to be installed
other modules: each module contains information about a specific package
    See beim.packages.Package for necessary attributes
"""


def factory(pypkg):
    bundles = _imp('bundles', pypkg)
    defaults = _imp('defaults', pypkg)

    # names of packages
    packageSequence = []
    for name in bundles.bundleNames:
        packageSequence += bundles.bundleInfo[name]
        continue

    # alias
    packageNames = packageSequence

    # a dictionary of {name: package}
    packageInfoTable = createTable( packageNames, pypkg )

    return Packages(packageInfoTable, packageNames)



def createTable(packageNames, pypkg):
    t = {}
    for name in packageNames:
        modname = name.replace( '-', '_' )
        m = _imp(modname, pypkg)
        t[name] = PackageProxy(m)
        continue
    return t



from ..Packages import Packages as base
class Packages(base):

    def __init__(self, name2package, names):
        self.name2package = name2package
        self.names = names
        return


    def getAll(self):
        names = self.names
        return [self.name2package[n] for n in names]


    def getPackage(self, name):
        return self.name2package[name]


from beim.package.Package import Package
class PackageProxy(Package):
    
    '''a proxy of a python module containing the
    information about a package acts like beim.package.Package
    '''

    def __init__(self, module):
        self._module = module
        for k in ['name', 'deps', 'repo', 'patch']:
            v = getattr(module, k, None)
            setattr(self, k, v)
        return
    

def _imp(module, pypkg):
    name = pypkg.__name__
    m = '%s.%s' % (name, module)
    return __import__(m, {}, {}, [''])


# version
__id__ = "$Id$"

# End of file 
