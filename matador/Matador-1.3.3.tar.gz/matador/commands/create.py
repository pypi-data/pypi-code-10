#!/usr/bin/env python
from .command import Command
from matador.session import Session
import os
import subprocess


def add_to_git(directory, message):
    subprocess.run([
        'git', '-C', directory, 'add', '-A'],
        stderr=subprocess.STDOUT,
        stdout=open(os.devnull, 'w'))

    subprocess.run([
        'git', '-C', directory, 'commit', '-m', message],
        stderr=subprocess.STDOUT,
        stdout=open(os.devnull, 'w'))


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

        add_to_git(
            Session.project_folder, 'Create ticket %s' % self.args.ticket)


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

        add_to_git(
            Session.project_folder, 'Create package %s' % self.args.package)


class AddTicketToPackage(Command):

    def _add_arguments(self, parser):
        parser.prog = 'matador add-t2p'

        parser.add_argument(
            '-t', '--ticket',
            type=str,
            required=True,
            help='Ticket name')

        parser.add_argument(
            '-p', '--package',
            type=str,
            required=True,
            help='Ticket name')

    def _execute(self):
        package_file = os.path.join(
            Session.project_folder, 'deploy', 'packages', self.args.package,
            'tickets.yml')

        with open(package_file, 'a') as f:
            f.write('- %s\n' % self.args.ticket)
            f.close()

        add_to_git(
            Session.project_folder,
            'Add ticket %s to package %s' % (
                self.args.ticket, self.args.package))


