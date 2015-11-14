#!/usr/bin/env python
"""usage: create-repo [--chdir DIR] <repodir>

Options:
    --chdir DIR      change to directory before evaluating repodir,
                     this is useful for http file servers which reside in
                     another folder

repodir is the path where the distros are stored in.

writes a drivedroid repo json file to stdout,
all paths are related to repopath."""

import json
import sys
from os import listdir,stat,chdir
from os.path import join,basename,isfile
def log(txt):
    sys.stderr.write(txt+'\n')

def main():
    from docopt import docopt
    args = docopt(__doc__)
    repodir = args['<repodir>']
    if args['--chdir']:
        chdir(args['--chdir'])

    print(json.dumps(gen_repo(repodir)))


def gen_repo(imgdir):
    repo = []
    for d in listdir(imgdir):
        dpath = join(imgdir,d)
        entry = { }
        releases = []
        entry['id'] = d.lower().replace(' ','')
        entry['name'] = d
        logopath = join(dpath,'logo.png')
        if isfile(logopath):
            entry['logo'] = logopath
        try:
            with open(urlpath) as up:
                entry['url'] = up.read().strip()
        except:
            entry['url'] = "http://url-not-provided/"

        releasepath = join(dpath,'releases')
        for f in listdir(releasepath):
            # remove the extension and split at _ , front is the version, back is arch
            version,_,arch = f.rpartition('.')[0].rpartition('_')
            # jump over (dban-)2.3.0 to get the real version
            if version.lower().startswith(d.lower()):
                version = version[len(d)+1:]
            isopath = join(releasepath,f)
            isosize = stat(isopath).st_size
            releases.append( {
                'version': version,
                'url': isopath,
                'size': isosize,
                'arch': arch })

        entry['releases'] = releases
        repo.append(entry)
    return repo


if __name__ == '__main__':
    main()
