import sys
import argparse
from .config import read_config, run_test_suite


def get_opts(argv=None):
    parser = argparse.ArgumentParser('preflight')
    parser.add_argument('-c', '--config', default='preflight.ini',
                        help='The location of the preflight.ini checklist')
    return parser.parse_args(argv)


def main():
    opts = get_opts()
    try:
        test_suite = read_config(opts.config)
    except OSError as err:
        if hasattr(err, 'filename') and err.filename:
            sys.stderr.write('{}: {}\n'.format(err.filename, err.strerror))
            raise SystemExit(1)
        else:
            raise
    run_test_suite(test_suite)


if __name__ == '__main__':
    main()
