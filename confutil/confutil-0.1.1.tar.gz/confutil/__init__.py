''' confutil

Configuration utility to ease navigation of local and system configurations
'''

import os
from tempfile import mkstemp
from .config import Config


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('project_name', help='Name of project with which '
                        'configuration paths will be derived')
    parser.add_argument('--output', '-o', help='output path of full '
                        'loaded configuration')
    args = parser.parse_args()
    conf = Config(args.project_name)
    output = args.output
    if output is None:
        _, output = mkstemp(prefix='confutil__')
    conf.write(output)
    if args.output is None:
        with open(output) as f:
            text = f.read()
        print(text)
        os.remove(output)
