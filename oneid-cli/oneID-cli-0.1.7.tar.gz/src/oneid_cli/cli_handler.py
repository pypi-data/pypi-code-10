import argparse

from services import Provision, Configure
from session import CLISession


def main():
    session = CLISession()
    handler = CLIHandler(session)
    handler.main()


class CLIHandler(object):
    """
    Run service (provision, configure) with provided arguments

    :param session: Session instance for credentials and configuration
    :type session: session.CLISession

    :Example:

    $ oneid-cli configure --dev-id <unique-id>
                          --dev-secret <secret from developer portal>
                          --project <optional project id>
    """
    def __init__(self, session):
        self._command_table = None
        self._argument_table = None
        self._session = session

    def _get_command_table(self):
        """
        Build a list of arguments from the available commands
        """
        if self._command_table is None:
            # Map the service commands to classes
            self._command_table = dict()
            self._command_table['configure'] = Configure(self._session)
            self._command_table['provision'] = Provision(self._session)

        return self._command_table

    def main(self):
        parser = argparse.ArgumentParser(description='Run oneID Services '
                                                     'from the command line')
        parser.add_argument('service',
                            choices=self._get_command_table().keys(),
                            help='oneID Service')
        parser.add_argument('--project-id',
                            required=True,
                            help='Specify a project using oneID project UUID')

        parsed_args, remaining_args = parser.parse_known_args()

        if parsed_args.project_id is not None:
            self._session.project = parsed_args.project_id

        command_table = self._get_command_table()

        return command_table[parsed_args.service].run(*remaining_args)


