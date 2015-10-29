#!/usr/bin/env python

# take a snap shot of current packages by recording the current revision in use


import subprocess as sp
import os

def take_snapshot(name):
    print('taking a snapshot %r ...' % name)
    # snapshot directory
    directory = 'packages-%s' % name
    print('output directory: %s' % directory)
    
    # make a copy
    args = ['svn', 'cp', 'packages', directory]
    print('running %r ...' % ' '.join(args))
    runCmd(args)

    import packages
    from beim.packages.factories.fromPyPackage import factory
    pkgs = factory(packages)
    packages = pkgs.getAll()
    from beim.package.repoutils import getRevision
    print('touching up modules ...')
    for package in packages:
        name = package.name
        print(' * %s' % name)
        rev = getRevision(package.repo)
        filename = '%s.py' % name
        path = os.path.join(directory, filename)
        stream = open(path, 'a')
        stream.write('revision=%s' % rev)
        stream.write('repo = repoutils.svn.getPackageRepository(reponame, branch, revision=revision, name=name)')
        continue
    return


def runCmd(args):
    p = sp.Popen(args)
    p.wait()
    if p.returncode:
        raise RuntimeError('cmd %s failed: %s' % (' '.join(args), p.returncode))
    return    


def main():
    import sys
    assert len(sys.argv)==2, "Syntax: take_snapshot <name>"
    
    name = sys.argv[1]
    take_snapshot(name)
    return


if __name__ == '__main__': main()
