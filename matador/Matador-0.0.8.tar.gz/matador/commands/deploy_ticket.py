#!/usr/bin/env python
from .command import Command
from matador import utils
import subprocess
import glob
import os
import shutil


class DeployTicket(Command):

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
            '-b', '--branch',
            type=str,
            default='master',
            help='Branch name')

        parser.add_argument(
            '-p', '--package',
            type=bool,
            default=False,
            help='Whether this deployment is part of a package')

    def _checkout_ticket(self, repo_folder, ticket_folder, branch):
        subprocess.run([
            'git', '-C', repo_folder, 'checkout', branch],
            stderr=subprocess.STDOUT,
            stdout=open(os.devnull, 'w'))
        src = os.path.join(repo_folder, 'deploy', 'tickets', self.args.ticket)
        shutil.copytree(src, ticket_folder)

    def _cleanup(self, ticket_folder):
        shutil.rmtree(ticket_folder)

    def _execute(self):
        project = utils.project()
        repo_folder = utils.matador_repository_folder(project)
        ticket_folder = os.path.join(
            utils.matador_ticket_folder(project, self.args.environment),
            self.args.ticket)

        if not self.args.package:
            utils.update_repository(project, self.args.branch)
        self._checkout_ticket(repo_folder, ticket_folder, self.args.branch)

        os.chdir(ticket_folder)
        import deploy

        self._cleanup(ticket_folder)
