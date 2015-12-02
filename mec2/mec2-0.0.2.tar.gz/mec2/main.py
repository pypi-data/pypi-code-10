#!/usr/bin/env python2.7
'''mec2 command line utility'''
import argparse
import mec2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='e.g. instance_id')
    args = parser.parse_args()
    fn = getattr(mec2, args.command, None)
    assert fn, 'Invalid command=' + args.command
    print fn()

if __name__ == '__main__':
    main()
