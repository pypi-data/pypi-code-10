#!/usr/bin/env python3

""" Keyword Substitution Script for Git
Based on the work by Peter Krusche at https://gist.github.com/pkrusche/7369262

Transforms stdin to expand some keywords with git version/date information.

Requires Python 3.

Specify --clean to remove this information before commit.

Setup:

1. Copy substitution.py into your git repository

2. Run:

 git config filter.substitution.smudge 'python3 substitution.py'
 git config filter.substitution.clean  'python3 substitution.py --clean'
 git add substitution.py

3. Add filters to .gitattributes:
e.g. to use substitution for all sql files:

 echo '*.sql filter=substitution' >> .gitattributes

3. Add substitution keywords to files as required:

 version:
 date:

4. Update the substitutions by deleting and then checking out the file.
"""
import sys
import subprocess
import re


def main():
    clean = False

    if len(sys.argv) > 1:
        if sys.argv[1] == '--clean':
            clean = True

    substitutions = {
        'version': None,
        'date': None,
    }

    if not clean:
        substitutions = {
            'version': subprocess.getoutput('git describe --always'),
            'date': subprocess.getoutput('git log --pretty=format:"%ad" -1'),
        }

        for key, value in substitutions.items():
            value = re.sub(r'[\n\r\t"\"]', '', value)

        for line in sys.stdin:
            for key, value in substitutions.items():
                rexp = '%s:' % key
                line = re.sub(rexp, '%s: %s' % (key, value), line)
            sys.stdout.write(line)

    else:
        for line in sys.stdin:
            for key in substitutions:
                rexp = '%s:.*' % key
                line = re.sub(rexp, '%s:' % key, line)
            sys.stdout.write(line)

if __name__ == '__main__':
    main()
