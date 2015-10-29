#!/usr/bin/env python
#
# Utility script to run pyflakes with the modules we care about and
# exclude errors we know to be fine.

import os
import re
import subprocess
import sys


def main():
    cur_dir = os.path.dirname(__file__)
    os.chdir(os.path.join(cur_dir, ".."))
    modules = sys.argv[1:]

    if not modules:
        modules = ['django_evolution']

    p = subprocess.Popen(['pyflakes'] + modules,
                         stderr=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         close_fds=True)

    contents = p.stdout.readlines()
    # Read in the exclusions file
    exclusions = {}
    fp = open(os.path.join(cur_dir, "pyflakes.exclude"), "r")

    for line in fp.readlines():
        if not line.startswith("#"):
            exclusions[line.rstrip()] = 1

    fp.close()

    # Now filter thin
    for line in contents:
        line = line.rstrip()
        test_line = re.sub(r':[0-9]+:', r':*:', line, 1)
        test_line = re.sub(r'line [0-9]+', r'line *', test_line)

        if test_line not in exclusions:
            print line


if __name__ == "__main__":
    main()
