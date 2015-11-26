#!/usr/bin/env python
import logging
import argparse
from matador.session import Session


class Command(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Taming the bull: Change management for Agresso systems")
        self._logger = logging.getLogger(__name__)
        self._add_arguments(parser)
        self.args, unknown = parser.parse_known_args()
        Session.initialise_session()
        self._execute()

    def _add_arguments(self, parser):
        pass

    def _execute(self):
        raise NotImplementedError
