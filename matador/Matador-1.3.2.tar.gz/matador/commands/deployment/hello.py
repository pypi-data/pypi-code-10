#!/usr/bin/env python
from .deployment import DeploymentCommand
import platform


class Hello(DeploymentCommand):

    def _execute(self):
        self._logger.info('Hello')
        self._logger.info(self.args[0])
        self._logger.info(platform.python_version())
