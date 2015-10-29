
import os


def checkoutCmd( server, repo, branch, revision=None, name=None ):
    '''checkoutCmd( "svn://danse.us", "histogram", "releases/DRCS-1.2" )
    '''
    if name is None: name = repo
    cmd = [ "svn co" ]
    if revision: cmd.append('-r %s' % revision)
    cmd.append(repourl(repo, branch, server=server))
    cmd.append(name)
    return ' '.join( cmd )


def updateCmd(revision=None):
    cmd = "svn update"
    if revision:
        cmd += ' -r %s' % revision
    return cmd


def repourl(repo, branch, server = 'svn://danse.us'):
    return "%(server)s/%(repo)s/%(branch)s" % locals()


def repoinfo( repo, branch, 
              server = "svn://danse.us", revision=None, name=None):
    if name is None: name = repo
    path = name # path to the checked-out stuff
    coCmd = checkoutCmd( server, repo, branch, revision=revision, name=name )
    upCmd = updateCmd(revision=revision)
    return path, coCmd, upCmd


import subprocess as sp
def iter_info(repourl):
    cmd = ['svn', 'info', repourl]
    p = sp.Popen(cmd, stdout=sp.PIPE)
    r = p.communicate()
    t = r[0]
    lines = t.splitlines()
    for line in lines:
        index = line.find(':')
        if index == -1: continue
        k = line[:index]
        v = line[index+1:]
        yield k,v
    return


def get_info(repourl):
    d = {}
    for k, v in iter_info(repourl):
        d[k] = v
    if not d:
        raise RuntimeError('failed to retrieve svn info for %s' % repourl)
    return d


def get_revision(repourl, server='svn://danse.us'):
    if server:
        repourl = server+'/'+repourl
    info = get_info(repourl)
    rev = info['Revision']
    return int(rev)
