# -*- coding: utf-8 -*-

import argparse

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command')
configure = subparsers.add_parser('configure')
configure.add_argument('input')
configure.add_argument('output')
args = parser.parse_args()

if args.command == 'configure':
    with open(args.input) as f:
        text = f.read()
    with open(args.output, 'w') as f:
        f.write(text)
