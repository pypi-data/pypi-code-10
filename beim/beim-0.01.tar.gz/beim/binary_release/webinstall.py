#!/usr/bin/env python


import os, sys

default_server="http://dev.danse.us/packages"


class DownloadError (Exception ): pass


def download( link, path ):
    print(" * Downloading %s to %s ... " % (link, path))
    localfileheader = 'file://'
    if link.startswith(localfileheader):
        cmd = "cd '%s' && cp %s ." % (path, link[len(localfileheader):])
        if os.system( cmd ):
            raise DownloadError("Failed to download %s" % link)
    else:
        filename = link[link.rfind('/')+1:]
        import os
        filepath = os.path.join(path, filename)
        fetchurl(link, filepath)

    return


def verify(path):
    f = open(path)
    for i in range(10):
        line = f.readline()
        if line.find('Object not found') != -1:
            raise RuntimeError('failed to load %s: %s' % (
                os.path.basename(path), line))
        continue
    return


def expand( tarball, path ):
    f = os.path.join( path, tarball ) 
    if not os.path.exists( f ) :
        raise  IOError("%s does not exist" % f)
    # save current dir
    curdir = os.path.abspath(os.curdir)
    # change to dest path
    os.chdir(path)
    # open tar ball and expand
    print(" * Expanding %s. This may take a while..." % tarball)
    import tarfile
    tar = tarfile.open(tarball)
    tar.extractall()
    tar.close() 
    # restore
    os.chdir(curdir)
    return


#  envs.sh
#replace the first line, this suppose that the first line
#is sth like ROOT=....
#and every line after are things like  PATH=$ROOT/bin:$PATH
def update_envs_sh( install_root ):
    path = os.path.join( install_root, 'bin', 'envs.sh' )
    newlines = [
        "root=%s\n" % install_root,
        ]
    _update_1st_line( path, newlines )
    return


def make_updates( install_root ):
    update_functions = [
        update_envs_sh,
        ]
    for f in update_functions: f( install_root )
    return



def fetchurl(url, path):
    import sys, urllib.request, urllib.parse, urllib.error
    #def reporthook(*a): print a
    def reporthook(*a): sys.stdout.write('.') ; sys.stdout.flush()
    print(url, "->", path)
    urllib.request.urlretrieve(url, path, reporthook)
    print()
    return


def _update_1st_line( path, newlines ):
    lines = open(path).readlines()
    found = -1
    for i,l in enumerate(lines):
        if l.startswith('root='): found = i; break
        continue
    if found == -1:
        raise RuntimeError("Cannot find a line starting with root=. lines=%r" % (
            '\n'.join( lines ), ))
    
    lines = newlines + lines[found+1:]
    open(path, 'w').writelines( lines )
    return



def main():
    from optparse import OptionParser

    parser = OptionParser(
        'usage: %prog [options] name path')
    parser.add_option(
        '-v', '--version', dest = 'version', default = 'default')
    parser.add_option(
        '-p', '--platform', dest = 'platform', default='linux2' )
    parser.add_option(
        '-y', '--python', dest = 'python', default='default' )
    parser.add_option(
        '-s', '--server', dest = 'server', default=default_server )

    argv = sys.argv
    opts, args = parser.parse_args( argv[1:] )

    try:
        name, path = args
    except Exception as error:
        print(parser.get_usage())
        sys.exit(1)
        return

    version = opts.version
    platform = opts.platform
    python = opts.python
    if python == 'default':
        vinfo = sys.version_info
        python = '.'.join( [ str(tok) for tok in vinfo[:2] ] )
        pass
    
    identifier = [
        name,
        version,
        platform,
        'py'+python,
        ]

    identifier = '-'.join( identifier )

    path = os.path.abspath(path)
    if not os.path.exists( path ): os.makedirs( path )

    tarball = "%s.tgz" % identifier
    server = opts.server
    link = '%s/%s' % (server, tarball)

    install_root = os.path.join( path, identifier )
    download( link, path )
    verify(os.path.join(path, tarball))

    expand( tarball, path )

    make_updates( install_root )

    print(" * Installation completed.")
    print()
    print("=============================")
    print("You will need to run the following command before you can use %(name)s-%(version)s software" % { 'name': name, 'version': version })
    print() 
    print("  $ . %s/bin/envs.sh" % install_root)
    print()
    print("You can add this command to your .bashrc so that it is executed automatically")
    return


if __name__ == "__main__": main()
