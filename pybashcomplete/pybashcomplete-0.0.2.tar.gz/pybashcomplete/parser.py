#!/usr/bin/env python

import os
import re
from glob import glob

RE_ARG = re.compile(r'.*\.add_argument\s*\(\s*[\'"]([^\'"]+)')


def read_script(path):
    args = []
    with open(path) as f:
        for line in f:
            m = RE_ARG.match(line)
            if m is not None:
                args += [m.group(1)]
    return args


def find_script_in_argv(argv):
    for word in argv:
        if word.lower().endswith('.py') and os.path.exists(word):
            return word


def match_last(last, args):
    possible = []
    for arg in args:
        if arg.startswith(last):
            possible += [arg]
    return possible


def print_possible_file(word):
    files = glob(word + '*')
    if not files:
        print('EMPTY:')
        return
    if len(files) == 1:
        print('COMPLETE:%s' % files[0])
        return
    print('MULTIPLE:%s' % ' '.join(files))


def main():
    import sys
    script = find_script_in_argv(sys.argv)
    if script is None:
        print_possible_file(sys.argv[-1])
        return
    args = read_script(script)
    possible_args = match_last(sys.argv[-1], args)
    if not possible_args:
        print('EMPTY:')
        return
    if len(possible_args) == 1:
        print('COMPLETE:%s' % possible_args[0])
    if len(possible_args) > 1:
        print('MULTIPLE:%s' % ' '.join(possible_args))


if __name__ == '__main__':
    main()
