# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2015 <contact@redhat.com>
#
# Author: Loic Dachary <loic@dachary.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see `<http://www.gnu.org/licenses/>`.
#
import argparse
from ceph_workbench import wbbackport
from ceph_workbench import wbbackportsetrelease
from github2gitlab import main
import logging
import os
import sys
import textwrap


class CephWorkbench(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="development workflow for Ceph")

        self.parser.add_argument(
            '-v', '--verbose',
            action='store_true', default=None,
            help='be more verbose',
        )

        self.parser.add_argument(
            '--libdir',
            help='directory containing helpers programs',
        )
        self.parser.add_argument(
            '--datadir',
            help='directory for persistent data',
        )

        subparsers = self.parser.add_subparsers(
            title='subcommands',
            description='valid subcommands',
            help='sub-command -h',
        )

        subparsers.add_parser(
            'github2gitlab',
            help='Mirror a GitHub project to GitLab',
            parents=[main.GitHub2GitLab.get_parser()],
            add_help=False,
        ).set_defaults(
            func=main.GitHub2GitLab,
        )

        subparsers.add_parser(
            'backport',
            help='Backport reports',
            parents=[wbbackport.WBBackport.get_parser()],
            add_help=False,
        ).set_defaults(
            func=wbbackport.WBBackport,
        )

        subparsers.add_parser(
            'backport-set-release',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=textwrap.dedent("""\
            Set the release field of backport issues.

            For each open issue in the Backport tracker, get the
            URL to pull request from the description. If the pull request
            is merged, get the version with git describe. The issue is
            then resolved and the version is set to the next minor version.

            Let say http://tracker.ceph.com/issues/12484 has the URL
            https://github.com/ceph/ceph/pull/5360 in its description
            and it was merged as commit
            4a1e54fc88e43885c57049d1ad4c5641621b6c29. git describe
            returns v0.80.10-165-g4a1e54f and the version field of
            issue 12484 is set to v0.80.11 which is the Ceph version
            in which the commit will be published.
            """),
            epilog=textwrap.dedent("""
            Example:

            ceph-workbench backport-set-release \\
                           --git-directory /tmp/ceph \\
                           --github-token $github_token \\
                           --redmine-key XXX \\
                           --dry-run
            """),
            help='Set the release field of the backport issues',
            parents=[wbbackportsetrelease.WBBackportSetRelease.get_parser()],
            add_help=False,
        ).set_defaults(
            func=wbbackportsetrelease.WBBackportSetRelease,
        )

    def run(self, argv):
        args = self.parser.parse_args(argv)

        if args.verbose:
            level = logging.DEBUG
        else:
            level = logging.INFO
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                            level=level)

        if not args.libdir:
            # sys.prefix is set by virtualenv
            if os.path.exists(sys.prefix + '/lib/ceph-workbench'):
                args.libdir = sys.prefix + '/lib/ceph-workbench'
            else:
                args.libdir = '/usr/local/lib/ceph-workbench'

        if not args.datadir:
            # sys.prefix is set by virtualenv
            if os.path.exists(sys.prefix + '/share/ceph-workbench'):
                args.datadir = sys.prefix + '/hsare/ceph-workbench'
            else:
                args.datadir = '/usr/local/share/ceph-workbench'

        return args.func(args).run()
