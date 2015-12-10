#!/usr/bin/env python
from .command import Command
from matador.commands.deployment import *
from matador.session import Session
import subprocess
import os
import shutil
from importlib.machinery import SourceFileLoader


def _checkout_ticket(ticket, repo_folder, ticket_folder, commit):

    subprocess.run([
        'git', '-C', repo_folder, 'checkout', commit],
        stderr=subprocess.STDOUT,
        stdout=open(os.devnull, 'w'),
        check=True)

    src = os.path.join(repo_folder, 'deploy', 'tickets', ticket)
    shutil.copytree(src, ticket_folder)


def execute_ticket(ticket, action, commit, packaged=False):
    proj_folder = Session.project_folder
    repo_folder = Session.matador_repository_folder
    ticket_folder = os.path.join(
        Session.matador_tickets_folder, ticket)
    Session.deployment_folder = ticket_folder

    shutil.rmtree(ticket_folder, ignore_errors=True)

    if not packaged:
        Session.update_repository()

    if commit == 'none':
        commit = subprocess.check_output(
            ['git', '-C', proj_folder, 'rev-parse', 'HEAD'],
            stderr=subprocess.STDOUT).decode('utf-8').strip('\n')

    _checkout_ticket(ticket, repo_folder, ticket_folder, commit)

    actionFile = action + '.py'
    sourceFile = os.path.join(ticket_folder, actionFile)
    SourceFileLoader(action, sourceFile).load_module()


class ActionTicket(Command):
    action = 'None'

    def _add_arguments(self, parser):
        parser.prog = 'matador deploy-ticket'
        parser.add_argument(
            '-e', '--environment',
            type=str,
            required=True,
            help='Agresso environment name')

        parser.add_argument(
            '-t', '--ticket',
            type=str,
            required=True,
            help='Ticket name')

        parser.add_argument(
            '-c', '--commit',
            type=str,
            default='none',
            help='Commit or tag ID')

        parser.add_argument(
            '-p', '--packaged',
            type=bool,
            default=False,
            help='Whether this deployment is part of a package')

    def _execute(self):
        Session.set_environment(self.args.environment)
        execute_ticket(self.args.ticket, self.action, self.args.commit, False)


class DeployTicket(ActionTicket):
    action = 'deploy'


class RemoveTicket(ActionTicket):
    action = 'remove'
