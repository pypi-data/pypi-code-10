#!/usr/bin/env python
from .command import Command
from matador import utils


class DeployTicket(Command):

    def _add_arguments(self, parser):
        parser.prog = 'matador deploy-ticket'
        parser.add_argument(
            '-e', '--environment',
            type=str,
            required=True,
            help='Agresso environment name')

    def _execute(self):
        project_folder = utils.project_folder()
        self._logger.info(project_folder)

        working_folder = utils.working_folder('uog01', self.args.environment)
        self._logger.info(working_folder)

        project = utils.project()
        self._logger.info(project)

        environments = utils.environments()
        self._logger.info(environments)
