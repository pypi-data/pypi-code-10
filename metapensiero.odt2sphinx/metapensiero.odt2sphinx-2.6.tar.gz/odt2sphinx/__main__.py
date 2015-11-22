# -*- coding: utf-8 -*-
# :Project:   metapensiero.odt2sphinx
# :Created:   Mar 10 nov 2015 17:51:31 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   Python Software Foundation License
# :Copyright: Copyright (C) 2015 Lele Gaifax
#

from difflib import unified_diff
from io import StringIO
from os.path import relpath
from pathlib import Path
import sys

from .odt import Reader
from .rst import Writer
from .visitor import Visitor


def test_output(writer, source):
    output = StringIO()
    original_stdout = sys.stdout
    sys.stdout = output
    try:
        writer.writeout()
    finally:
        sys.stdout = original_stdout

    output.seek(0)
    generated = output.getvalue().splitlines(keepends=True)

    expected_rst = source.with_suffix('.expected.rst')
    try:
        with expected_rst.open() as f:
            expected = f.read().splitlines(keepends=True)
    except FileNotFoundError:
        sys.stderr.write('Could not load expected text from %s\n' % expected_rst)
        sys.exit(2)

    diff = list(unified_diff(expected, generated, str(expected_rst), "generated"))
    if diff:
        sys.stdout.writelines(diff)
        sys.exit(1)


def odt_to_sphinx(source, target, encoding, download_source_link=False,
                  embedded_uris=False, debug=False, test=False):
    if test:
        target = '-'

    reader = Reader(source, debug)

    if download_source_link:
        download_source_link = Path(relpath(str(source), str(target)))

    writer = Writer(target, encoding, download_source_link, embedded_uris, debug)

    visitor = Visitor(writer, debug)

    reader(visitor)

    if test:
        test_output(writer, source)
    else:
        writer.writeout()


def test(source, **other_args):
    if source.is_dir():
        sources = sorted(source.glob('*.odt'))
    else:
        sources = (source,)

    for source in sources:
        expected_rst = source.with_suffix('.expected.rst')
        if expected_rst.exists():
            sys.stderr.write('Checking %s...' % source)
            odt_to_sphinx(source, **other_args)
            sys.stderr.write(' ok\n')
        else:
            sys.stderr.write('Cannot check %s, no corresponding %s\n' %
                             (source, expected_rst))


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser(description="ODT to RST")

    parser.add_argument('--debug', dest='debug', action='store_true', default=False,
                        help='Emit debug noise')
    parser.add_argument('--download-source-link', dest='download_source_link',
                        action='store_true', default=False,
                        help='Add a link to the ODT source file')
    parser.add_argument('--embedded-uris', action='store_true', default=False,
                        help='Emit embedded URIs, instead of anonymous refs')
    parser.add_argument('--encoding', type=str, default='utf-8',
                        help='Output encoding, by default UTF-8')
    parser.add_argument('--test', default=False, action='store_true',
                        help='Run in test mode, comparing output with expected reST'
                        ' to be found in “source.expected.rst”')
    parser.add_argument('source', type=Path,
                        help='Source ODT file to be converted, or a directory containing'
                        ' ODT files and corresponding .expected.rst files in test mode')
    parser.add_argument('target', nargs='?', default='-',
                        help='Either destination directory, a single .rst target filename'
                        ' or "-" for stdout')

    args = parser.parse_args()

    if args.target != '-':
        args.target = Path(args.target)

    if args.test:
        test(**args.__dict__)
    else:
        odt_to_sphinx(**args.__dict__)


if __name__ == '__main__':
    main()
