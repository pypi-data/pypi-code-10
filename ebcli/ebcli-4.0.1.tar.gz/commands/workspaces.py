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

import commands


def initialize_parser(subparsers):
    parser = subparsers.add_parser('workspaces', help='List workspaces')

    commands.add_standard_argument(parser, commands.FIELDS_ARG, default=commands.DEFAULT_WORKSPACE_FIELDS)
    parser.set_defaults(func=execute_command)


def execute_command(args, _unknown):
    session = commands.AuthenticatedSession(args.url, args.token)
    workspaces = session.get('/services/workspaces').json()

    formatter = commands.Formatter(args)
    formatter.write(workspaces, prefix='WORKSPACE', fields=args.fields)
