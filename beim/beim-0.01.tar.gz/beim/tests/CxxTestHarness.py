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


    class BinaryMissing(base.TestRunFailure):

        def __init__(self, src):
            super().__init__(src, "Missing binary")


    def runtest(self, src, dry_run=False):
        import os
        
        self.log('* %s' % src)

        # binary
        bin = findCorrespondingBinary(src)
        if not os.path.exists(bin): raise self.BinaryMissing(src)
        
        dirname = os.path.dirname(bin)
        fn = os.path.basename(bin)
        cmd = './%s' % (fn,)
        if dry_run:
            self.log("* running %s in %s" % (cmd, dirname))
            return
        from ..osutils import execute
        code, out, err = execute(cmd, cwd=dirname)
        if code:
            err = '%s failed: out:\n%serr:\n%s' % (
                src, out, err)
            raise self.TestRunFailure(test=src, error=err)
        return

    @classmethod
    def createReport(cls, sources, failed):
        # split failures into nobinaries and others
        allfailures = failed
        nobinaries = []; failed = []
        for f in allfailures:
            if isinstance(f, cls.BinaryMissing):
                nobinaries.append(f)
            else:
                failed.append(f)

        #
        print()
        print("Report:")
        if not nobinaries and not failed:
            print('* SUCCEED:   %s tests passed' % len(sources))
            return

        npassed = len(sources) - len(nobinaries) - len(failed)
        s = '* Failed. Out of %s tests, %s passed, ' % (len(sources), npassed)
        if nobinaries:
            s += '%s have no test binaries,' % (len(nobinaries),)
        if failed:
            s += '%s failed' % (len(failed),)
        print(s)

        if nobinaries:
            print(" - no binaries:")
            for item in nobinaries:
                print(item.test)

        if failed:
            print(" - failed:")
            for item in failed:
                print(item.test)
        return
    

def findCorrespondingBinary(src):
    # XXX: this assume that binary filename is simply the source filename minus extension
    import os
    base, ext = os.path.splitext(src)
    return base


# version
__id__ = "$Id$"

# End of file 
