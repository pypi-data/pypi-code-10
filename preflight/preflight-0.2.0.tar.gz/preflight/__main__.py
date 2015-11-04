import sys
import argparse
from .config import build_test_suite_from_file, run_test_suite
from .exceptions import BadConfigException


def get_opts(argv=None):
    parser = argparse.ArgumentParser('preflight')
    parser.add_argument('-c', '--config', default='preflight.ini',
                        help='The location of the preflight.ini checklist')
    parser.add_argument('-p', '--profile', default=None,
                        help='The site profile to use. Defaults to the first profile defined')
    return parser.parse_args(argv)


def run(opts):
    try:
        config_file = open(opts.config, 'r')
    except OSError as err:
        if hasattr(err, 'filename') and err.filename:
            sys.stderr.write('{}: {}\n'.format(err.filename, err.strerror))
            raise SystemExit(1)
        else:
            raise

    try:
        test_suite = build_test_suite_from_file(config_file, profile=opts.profile)
    except BadConfigException as err:
        sys.stderr.write('{}: {}\n'.format(opts.config, err.args[0]))
        raise SystemExit(1)
    run_test_suite(test_suite)


def main():
    run(get_opts())


if __name__ == '__main__':
    main()
