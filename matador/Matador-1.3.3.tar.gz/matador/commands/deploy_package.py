#!/usr/bin/env python
from .command import Command
from .deploy_ticket import execute_ticket
from matador.session import Session
import subprocess
import os
import shutil
import yaml
from importlib.machinery import SourceFileLoader


class ActionPackage(Command):

    def _add_arguments(self, parser):
        parser.prog = 'matador deploy-package'
        parser.add_argument(
            '-e', '--environment',
            type=str,
            required=True,
            help='Agresso environment name')

        parser.add_argument(
            '-p', '--package',
            type=str,
            required=True,
            help='Package name')

        parser.add_argument(
            '-c', '--commit',
            type=str,
            default='none',
            help='Commit or tag ID')

    @staticmethod
    def _checkout_package(package, commit):
        proj_folder = Session.project_folder
        repo_folder = Session.matador_repository_folder
        package_folder = os.path.join(
            Session.matador_packages_folder, package)

        shutil.rmtree(package_folder, ignore_errors=True)

        Session.update_repository()

        if commit == 'none':
            commit = subprocess.check_output(
                ['git', '-C', proj_folder, 'rev-parse', 'HEAD'],
                stderr=subprocess.STDOUT).decode('utf-8').strip('\n')

        subprocess.run([
            'git', '-C', repo_folder, 'checkout', commit],
            stderr=subprocess.STDOUT,
            stdout=open(os.devnull, 'w'),
            check=True)

        src = os.path.join(repo_folder, 'deploy', 'packages', package)
        shutil.copytree(src, package_folder)

    def _execute(self):
        Session.set_environment(self.args.environment)
        self._checkout_package(self.args.package, self.args.commit)


class DeployPackage(ActionPackage):

    def _execute(self):
        super(DeployPackage, self)._execute()
        package_folder = os.path.join(
            Session.matador_packages_folder, self.args.package)
        Session.deployment_folder = package_folder
        ticketsFile = os.path.join(package_folder, 'tickets.yml')

        tickets = yaml.load(open(ticketsFile, 'r'))
        for ticket in tickets:
            self._logger.info('*' * 25)
            self._logger.info('Deploying ticket %s' % ticket)
            self._logger.info('*' * 25)
            execute_ticket(str(ticket), 'deploy', self.args.commit, True)



class RemovePackage(ActionPackage):

    def _execute(self):
        super(RemovePackage, self)._execute()
        package_folder = os.path.join(
            Session.matador_packages_folder, self.args.package)
        Session.deployment_folder = package_folder
        sourceFile = os.path.join(package_folder, 'remove.py')

        SourceFileLoader('remove', sourceFile).load_module()
