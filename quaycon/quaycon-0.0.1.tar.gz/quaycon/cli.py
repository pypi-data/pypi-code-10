import argparse
from getpass import getpass
import logging
import sys

from . api import QuayCon
from . errors import (
    MissingTokenError,
    UnknownOrganization,
)
from . utils import QUAYIO_REGISTRY
from . config import load_config
from . utils import ask_confirmation, parse_repository


def touch_command(repository, config_file, **kwargs):
    registry, org, name, tag = parse_repository(repository)
    config = load_config(config_file)
    quaycon = QuayCon(config)
    return list(quaycon.touch(registry, org, name, tag, **kwargs))


def discover_command(organizations, config_file, **kwargs):
    config = load_config(config_file)
    quaycon = QuayCon(config)
    organizations = organizations or quaycon.organizations
    for org in organizations:
        try:
            quaycon.discover(org)
        except (MissingTokenError, UnknownOrganization):  # pragma: no cover
            if not kwargs.setdefault('interactive', True):
                raise
            msg = "Unknown organization '{}'. Do you wish to add it?"
            if ask_confirmation(msg.format(org)):
                token = getpass("Please enter API token: ")
                quaycon.add_organization(QUAYIO_REGISTRY, org, token)
                quaycon.save()
                quaycon.discover(org)
    if kwargs.setdefault('interactive', True):
        quaycon.save()


def version_command(*args, **kwargs):  # pragma: no cover
    from . import __version__
    version = '.'.join(map(str, __version__))
    sys.stdout.write(version + '\n')


def main(*args):  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v', '--verbose',
        action='count',
        help='Verbose mode, -vv for more details'
    )
    parser.add_argument(
        '-c', '--config',
        dest='config_file',
        help='Specify configuration file'
    )
    subparsers = parser.add_subparsers(help='sub-command help')
    version_parser = subparsers.add_parser(
        'version', help='print software version'
    )
    version_parser.set_defaults(func=version_command)

    touch_parser = subparsers.add_parser(
        'touch', help='trigger dependant builds'
    )
    touch_parser.add_argument(
        '-w', '--wait',
        type=int,
        default=0,
        help='Delay in seconds between build status checks. Default is 0'
             'meaning that command does not wait for build completion'
    )
    touch_parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        default=False,
        help='Rebuild entire sub-tree dependencies.'
    )
    touch_parser.add_argument('repository')
    touch_parser.set_defaults(func=touch_command)

    discover_parser = subparsers.add_parser(
        'discover', help='Discover dependencies between repositories'
    )
    discover_parser.add_argument(
        'organizations', metavar='ORG', nargs='*',
        default=None, help='Organizations sub-set to inspect'
    )
    discover_parser.set_defaults(func=discover_command)

    args = parser.parse_args()
    logging_level = logging.WARN
    if args.verbose == 1:
        logging_level = logging.INFO
    elif args.verbose == 2:
        logging_level = logging.DEBUG
    elif args.verbose > 2:
        logging_level = logging.TRACE
    logging.basicConfig(level=logging_level)
    for logger in ['requests']:
        logging.getLogger(logger).setLevel(logging.WARNING)
    args.func(**vars(args))
