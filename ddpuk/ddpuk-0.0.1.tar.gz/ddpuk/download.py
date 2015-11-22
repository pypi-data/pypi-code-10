#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Download data from http://lda.data.parliament.uk"""

from __future__ import division, print_function, absolute_import

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import codecs
import logging
from os import mkdir, path
import requests
import sys

from ddpuk import __version__   # noqa: make available

__author__ = "Florian Rathgeber"
__copyright__ = "Florian Rathgeber 2015"
__license__ = "mit"

log = logging.getLogger(__name__)

BASEURL = 'http://lda.data.parliament.uk'
URL = BASEURL + r'/%(data)s.%(format)s?_pageSize=%(size)d&_page=%(page)d'
MAX_PAGE = 125
SIZE = 500


def download(dataset, fmt='json', size=SIZE, page_from=0, page_to=MAX_PAGE,
             datadir='data'):
    if not path.exists(datadir):
        mkdir(datadir)
    for page in range(page_from, page_to):
        log.info('downloading page %d/%d', page + 1, page_to + 1)
        url = URL % {'data': dataset, 'format': fmt, 'size': size, 'page': page}
        log.info('  %s', url)
        r = requests.get(url)
        fname = path.join(datadir, '%s-%d-%05d.%s' % (dataset, size, page, fmt))
        with codecs.open(fname, 'w', 'utf-8') as f:
            f.write(r.text)


def parse_args(args=None):
    """
    Parse command line parameters

    :param args: command line parameters as list of strings
    :return: command line parameters as :obj:`airgparse.Namespace`
    """
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('dataset', help='dataset to download')
    parser.add_argument('--format', dest='fmt', default='json', help='format',
                        choices=['csv', 'json', 'rdf', 'text', 'ttl', 'xml'])
    parser.add_argument('--size', type=int, default=SIZE, help='batch size')
    parser.add_argument('--page-from', type=int, default=0, help='first page')
    parser.add_argument('--page-to', type=int, default=MAX_PAGE, help='last page')
    parser.add_argument('--datadir', default='data', help='target directory')
    return parser.parse_args(args)


def main():
    download(**vars(parse_args()))


def run():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()


if __name__ == "__main__":
    run()
