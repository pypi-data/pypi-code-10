#!/usr/bin/env python
"""
ElasticBox Confidential
Copyright (c) 2015 All Right Reserved, ElasticBox Inc.

NOTICE:  All information contained herein is, and remains the property
of ElasticBox. The intellectual and technical concepts contained herein are
proprietary and may be covered by U.S. and Foreign Patents, patents in process,
and are protected by trade secret or copyright law. Dissemination of this
information or reproduction of this material is strictly forbidden unless prior
written permission is obtained from ElasticBox
"""

import argparse
import sys
import keyring
import logging

import commands.boxes
import commands.build
import commands.delete
import commands.deploy
import commands.get
import commands.export
import commands.import_box
import commands.instances
import commands.login
import commands.logout
import commands.poweron
import commands.reconfigure
import commands.reinstall
import commands.set
import commands.shutdown
import commands.terminate
import commands.workspaces

DEFAULT_ELASTICBOX_URL = 'https://elasticbox.com'


def main():
    debug = False

    try:
        parser = argparse.ArgumentParser(
            description='ElasticBox commands',
            epilog="See 'ebcli command --help' for more information")

        parser.add_argument('--url', help='Host to connect', default=DEFAULT_ELASTICBOX_URL)
        parser.add_argument('--token', help='Authentication Token')
        parser.add_argument('--debug', action='store_true', default=False)
        parser.add_argument('--verbose', action='store_true', default=False)
        parser.add_argument('-j', '--json', action='store_true', default=False)

        credentials = keyring.get_password(commands.ELASTICBOX_CREDENTIALS_NAME,
                                           commands.ELASTICBOX_CREDENTIALS_ACCOUNT)
        if credentials:
            token, url = credentials.split(',')
            parser.set_defaults(token=token, url=url)
        else:
            token = None
            url = DEFAULT_ELASTICBOX_URL

        subparsers = parser.add_subparsers(title='Commands', dest='command')

        _initialize_commands(subparsers)

        args, unknown_args = parser.parse_known_args()

        if 'debug' in args and debug:
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(formatter)
            root = logging.getLogger()
            root.addHandler(handler)
            root.setLevel(logging.DEBUG)
            handler.setLevel(logging.DEBUG)

        if not args.token:
            if args.command != 'login':
                raise commands.AuthTokenException('Need to authenticate before using the command line')
        else:
            # Reset token if the url is different that the one stored
            if args.command == 'login' and args.url != url and token and not args.token:
                args.token = None

        args.func(args, unknown_args)

    except commands.AuthTokenException, auth:
        print >> sys.stderr, commands.TermColors.FAIL + auth.message + commands.TermColors.ENDC
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(1)
    except commands.ApiException, api:
        logging.exception(api)
        print >> sys.stderr, commands.TermColors.FAIL + api.message + commands.TermColors.ENDC

        sys.exit(2)
    except Exception, ex:
        logging.exception(ex)
        print >> sys.stderr, commands.TermColors.FAIL + ex.message + commands.TermColors.ENDC

        sys.exit(1)

    sys.exit(0)


def _initialize_commands(subparsers):
    commands.boxes.initialize_parser(subparsers)
    commands.build.initialize_parser(subparsers)
    commands.delete.initialize_parser(subparsers)
    commands.deploy.initialize_parser(subparsers)
    commands.get.initialize_parser(subparsers)
    commands.export.initialize_parser(subparsers)
    commands.import_box.initialize_parser(subparsers)
    commands.instances.initialize_parser(subparsers)
    commands.login.initialize_parser(subparsers)
    commands.logout.initialize_parser(subparsers)
    commands.set.initialize_parser(subparsers)
    commands.poweron.initialize_parser(subparsers)
    commands.reconfigure.initialize_parser(subparsers)
    commands.reinstall.initialize_parser(subparsers)
    commands.shutdown.initialize_parser(subparsers)
    commands.terminate.initialize_parser(subparsers)
    commands.workspaces.initialize_parser(subparsers)


if __name__ == '__main__':
    main()
