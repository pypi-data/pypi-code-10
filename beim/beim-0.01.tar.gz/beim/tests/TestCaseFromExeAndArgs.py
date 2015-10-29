#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

        
import unittest


class Target(object):

    args = []
    env = {}


    def __init__(self, args=None, env = None):
        self.args = args or []
        self.env = env or {}
        return


class TestCaseBase(unittest.TestCase):


    cmd = None
    targets = []

    def runTarget(self, target):
        args = target.args
        cmd = [self.cmd] + args
        cmd = ' '.join(cmd)
        
        env = target.env
        retcode, outdata, errdata = execute(cmd, cwd='.', env=env)
        if retcode:
            raise RuntimeError("failed to run %s" % cmd)
        return


def cmdline(cmd, target):
    return '$ %s %s' % (cmd, ' '.join(target.args))


class TestCaseFactory(object):

    def build(self, cmd, targets):
        """
        targets: a list of targets
        target: a Target instance
        """
        indent = '  '
        class TestCase(TestCaseBase): 
            
            for i, target in enumerate(targets):
                name = 'test%s' %i
                help = '"""' + cmdline(cmd, target) + '"""'
                code = 'def %s(self):\n%s%s\n%sreturn self.runTarget(self.targets[%s])' % (
                    name, indent, help, indent, i)
                exec(code)

        TestCase.cmd = cmd
        TestCase.targets = targets
        return TestCase


import shlex, subprocess

def spawn(cmd, cwd=None, env=None, stdin=None, stdout=None, stderr=None):
    '''spawn a new process

    cmd: the command to execute in the new process
    cwd: the directory where the command will be executed
    env: the environment dictionary
    stdin, stdout, stderr:

    return: new process
    '''
    args = shlex.split(cmd)
    p = subprocess.Popen(args, cwd=cwd, env=env, stdin=stdin, stdout=stdout, stderr=stderr)
    return p


def execute(cmd, input=None, cwd=None, env=None):
    '''execute a command and return the returncode, stdout data, and stderr data
    '''
    # print '* executing %r...' % cmd
    p = spawn(
        cmd, cwd=cwd, env=env,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
    outdata, errdata = p.communicate(input=input)
    retcode = p.wait()
    return retcode, outdata, errdata


# version
__id__ = "$Id$"

# End of file 
