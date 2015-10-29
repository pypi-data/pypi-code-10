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


from ..tests.PyTestHarness import TestHarness


def runtests(root='.', dry_run=False):
    testharness = TestHarness(root=root)
    return testharness.run(dry_run=dry_run)


createReport = TestHarness.createReport


def main():    
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('-d', '--dry-run', action='store_true', dest='dry')
    opts, args = parser.parse_args()
    
    dry = opts.dry

    # root
    if args:
        assert len(args) == 1
        root = args[0]
    else:
        root = '.'
    
    tests, failed = runtests(dry_run=dry, root=root)
    createReport(sources=tests, failed=failed)
    if failed:
        import sys
        sys.exit(1)
    
    return


# End of file 
