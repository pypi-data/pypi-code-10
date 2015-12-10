#!/usr/bin/env python
from .command import Command
from matador.session import Session
import os


class CreateTicket(Command):

    def _add_arguments(self, parser):
        parser.prog = 'matador create-ticket'

        parser.add_argument(
            '-t', '--ticket',
            type=str,
            required=True,
            help='Ticket name')

    def _execute(self):
        ticket_folder = os.path.join(
            Session.project_folder, 'deploy', 'tickets', self.args.ticket)
        os.makedirs(ticket_folder)
        deploy_file = os.path.join(ticket_folder, 'deploy.py')
        with open(deploy_file, 'w') as f:
            f.write('from matador.commands.deployment import *\n\n')
            f.close()


class CreatePackage(Command):

    def _add_arguments(self, parser):
        parser.prog = 'matador create-package'

        parser.add_argument(
            '-p', '--package',
            type=str,
            required=True,
            help='Ticket name')

    def _execute(self):
        package_folder = os.path.join(
            Session.project_folder, 'deploy', 'packages', self.args.package)
        os.makedirs(package_folder)

        package_file = os.path.join(package_folder, 'tickets.yml')
        with open(package_file, 'w') as f:
            f.write(
                '# List each ticket on a separate line preceded by - . e.g.\n')
            f.write('# - 30\n')
            f.write('# - 31\n')
            f.close()

        remove_file = os.path.join(package_folder, 'remove.py')
        with open(remove_file, 'w') as f:
            f.write('from matador.commands.deployment import *\n\n')
            f.close()
