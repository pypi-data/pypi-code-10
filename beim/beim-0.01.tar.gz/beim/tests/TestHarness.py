# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


"""
base class for test harness
"""


import os


class TestHarness(object):

    configfilename = '.tests.beimconfig'

    # exceptions
    class TestRunFailure(Exception):
        
        def __init__(self, test=None, error=None):
            super().__init__(error)
            self.test = test
            return

    # meta methods
    def __init__(self, root=None, configuration=None):
        """path to the root of a directory tree in which tests will be
        searched for
        """
        if root is None:
            import os
            root = os.curdir
        self.root = root
        self.configuration = configuration or self._loadConfiguration(root)
        return
    
        
    # methods
    def run(self, dry_run=False):
        tests = self.findTests()
        failed = []
        for test in tests:
            try:
                self.runtest(test, dry_run=dry_run)
            except self.TestRunFailure as e:
                failed.append(e)
            continue
        return tests, failed


    @classmethod
    def createReport(cls, tests, failed):
        """create a report

        * tests: tests ran
        * failed: test failures
        """
        raise NotImplementedError


    def findTests(self):
        """find the tests
        """
        filter = self.configuration['testfile_filter']
        return find(self.root, filter)


    def runtest(self, test, dry_run=False):
        """run one test. in case of failure, raise an exception of TestRunFailed
        """
        raise NotImplementedError


    def log(self, msg):
        print (msg)


    def _loadConfiguration(self, root):
        configfile = os.path.join(root, self.configfilename)
        if os.path.exists(configfile):
            from .config_utils import load
            return load(configfile)
        else:
            e = "test configuration file %s does not exist" % (configfile,)
            raise IOError(e)
                
        return
    

def find(root, filter):
    """find files in a directory tree

    root: root path of the directory tree
    filter: method to tell whether a filename is a good one
    """
    rt = []
    for root, dirnames, filenames in os.walk(root):
        for filename in [f for f in filenames if filter(f)]:
            rt.append(os.path.join(root, filename))
    return rt

# version
__id__ = "$Id$"

# End of file 
