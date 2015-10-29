
import os


def checkoutCmd( server, repo, branch, revision=None, name=None ):
    '''checkoutCmd( "bzr+ssh://pyre.cacr.caltech.edu", "home/projects/pyre/web/repository", "1.0/pyre.db-jiao-experiment")
    '''
    if name is None: 
        raise ValueError("name is None")
    cmd = [ "bzr branch" ]
    if revision: cmd.append('-r %s' % revision)
    cmd.append("%(server)s/%(repo)s/%(branch)s %(name)s" % locals())
    return ' '.join( cmd )


def updateCmd(revision=None):
    cmd = "bzr pull"
    if revision:
        cmd += ' -r %s' % revision
    return cmd


def repourl(repo, branch, server = 'bzr://danse.us'):
    return "%(server)s/%(repo)s/%(branch)s" % locals()


def repoinfo( repo, branch, server = None, revision=None, name=None ):
    if name is None: 
        raise ValueError("name is None")
    path = name # path to the checked-out stuff
    coCmd = checkoutCmd( server, repo, branch, revision=revision, name=name )
    updateCmd = "bzr update"
    return path, coCmd, updateCmd
    
