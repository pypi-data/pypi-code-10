#!/usr/bin/env python
"""usage: create-repo [--chdir DIR] <repodir>

Options:
    --chdir DIR      change to directory before evaluating repodir,
                     this is useful for http file servers which reside in
                     another folder

repodir is the path where the distros are stored in.

writes a drivedroid repo json file to stdout,
all paths are related to repopath.

File structure looks like this:

    images/<name>
                /[logo.png] (96x96)
                /URL < contains uri of main website
                /releases/(<name>-)<version>_<arch>.(iso|img)

"""

import json
import sys
from os import listdir,stat,chdir
from os.path import join,basename,isfile,exists
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
        log("found distro {}".format(d))
        dpath = join(imgdir,d)
        entry = { }
        releases = []
        entry['id'] = d.lower().replace(' ','')
        entry['name'] = d
        logopath = join(dpath,'logo.png')
        if isfile(logopath):
            entry['logo'] = logopath
            log("found logo for distro {}".format(logopath))
        try:
            with open(join(dpath,'URL')) as up:
                entry['url'] = up.read().strip()
        except Exception as e:
            log("No url file found for {} - {}".format(d,e))
            entry['url'] = "http://url-not-provided/"

        releasepath = join(dpath,'releases')

        if not exists(releasepath):
            log("ERROR: {} does not have a release path!")
        else:
            for f in listdir(releasepath):
                try:
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
                    log("for {} - found Release {}".format(d,f))
                    log("  -> {}".format(releases[-1]))
                except Exception as e:
                    log("could not add release {} for distro {}".format(d,f))
                    log("Reason: {}".format(e))


        entry['releases'] = releases
        repo.append(entry)
    return repo

if __name__ == '__main__':
    main()
