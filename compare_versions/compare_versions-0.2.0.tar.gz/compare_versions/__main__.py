import argparse
import sys

from . import version
from . import core
from . import schemes

class InputError(Exception):
    # Denotes bad program input
    pass

def main():
    """
    Module entry point

    Run with "python -m compare_versions"
    """
    parser = argparse.ArgumentParser(description='compare_versions %s' % version.__version__)
    parser.add_argument('versions', nargs='*', help='version strings to compare')
    parser.add_argument('-s', '--scheme', default='semver', help='versioning scheme - semver[default]/string')
    parser.add_argument('-l', '--list', action='store_true', help='verify that a list of versions is in order according to "comparison"')
    parser.add_argument('-c', '--comparison', default='lt', help='expected ordering for "list" - one of eq/ne/gt/lt[default]/ge/le')
    args = parser.parse_args()

    if args.scheme not in schemes.schemes:
        raise InputError('Invalid versioning scheme "%s" - options are %s' % (args.scheme, '/'.join(s for s in schemes.schemes)))

    if args.comparison not in core.VALID_COMPARISONS:
        raise InputError('Invalid comparison "%s" - options are %s' % (args.comparison, '/'.join(c for c in core.VALID_COMPARISONS)))

    if len(args.versions) == 0:
        # Read from stdin until EOF
        content = sys.stdin.read()
        # Break on spaces and/or newlines
        versions = content.split()
    else:
        versions = args.versions

    if args.list:
        return core.verify_list(versions, args.comparison, scheme=args.scheme)

    else:
        if len(versions) < 2:
            raise InputError('Requires two versions to compare')
        v1 = schemes.schemes[args.scheme](versions[0])
        v2 = schemes.schemes[args.scheme](versions[1])
        print('%s %s %s' % (v1, core.comparison_symbol(v1, v2), v2))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
    except InputError as e:
        sys.stderr.write('%s\n' % e.message)
        sys.exit(1)
    except Exception as e:
        sys.stderr.write('%s: %s\n' % (type(e).__name__, e.message))
        sys.exit(1)

