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



from .TestHarness import TestHarness as base
class TestHarness(base):


    def __init__(self, py_exe=None, root=None, configuration=None):
        super().__init__(root=root, configuration=configuration)
        
        if py_exe is None:
            import sys
            py_exe = sys.executable
        self.py_exe = py_exe
        return
    

    def runtest(self, test, dry_run=False):
        from ..osutils import execute
        import os
        self.log('* %s' % test)
        dirname = os.path.dirname(test)
        fn = os.path.basename(test)
        cmd = '%s %s' % (self.py_exe, fn,)
        if dry_run:
            self.log("* running %s in %s" % (cmd, dirname))
            return
        code, out, err = execute(cmd, cwd=dirname)
        if code:
            err = '%s failed: out:\n%serr:\n%s' % (
                test, out.decode(), err.decode())
            print(err)
            raise self.TestRunFailure(test=test, error=err)
        return

    @classmethod
    def createReport(cls, sources, failed):
        print()
        print("Report:")
        if not failed:
            print('* SUCCEED:   %s tests passed' % len(sources))
            return

        npassed = len(sources) - len(failed)
        s = '* Failed. Out of %s tests, %s passed, ' % (len(sources), npassed)
        if failed:
            s += '%s failed' % (len(failed),)
        print(s)

        if failed:
            print(" - failed:")
            for item in failed:
                print(item.test)
                
        return
    

# version
__id__ = "$Id$"

# End of file 
