#!/usr/bin/env python
# coding: utf-8

"""Usage: colordesk [options] FILE

Process FILE to show its color palettes in a web page.

Arguments:
  FILE        a yaml file that contains color palettes definitions.

Options:
  -h --help
  -p PORT --port=PORT   port for web server to listen [default: 8888]
  -d --debug            enter debug mode
"""

import sys
from docopt import docopt
from .server import run


def main():
    args = docopt(__doc__)

    filename = args['FILE']
    filedict = {
        'name': filename,
    }
    try:
        with open(filename, 'r') as f:
            filedict['text'] = f.read()
    except IOError as e:
        print 'Could not read file {}: {}'.format(filename, e)
        sys.exit(1)

    run(filedict, debug=args['--debug'], port=args['--port'])
