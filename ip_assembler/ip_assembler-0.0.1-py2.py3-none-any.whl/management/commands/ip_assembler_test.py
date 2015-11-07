from django.core.management.base import BaseCommand, CommandError

from ip_assembler.models import IP
from ip_assembler.tasks import (
    IPEMailChecker,
    UpdateHtaccessLocationsTask,
    UpdateLocationsIfNecessaryTask,
)


class Command(BaseCommand):
    """
    Helper command for testing several functionality.
    """

    def handle(self, *args, **options):
        commands = {
            'email_checker_task': {
                'help': 'Runs the IPEMailChecker task.',
                'method': self.email_checker_task,
            },
            'unify_ips': {
                'help': 'Runs IP.unify_ips().',
                'method': self.unify_ips,
            },
            'location_replacement': {
                'help': 'UpdateHtaccessLocationsTask',
                'method': self.location_replacement,
            },
            'update_locations': {
                'help': 'UpdateLocationsIfNecessaryTask',
                'method': self.update_locations,
            }
        }

        if len(args) == 0:
            raise CommandError(
                'Please specify a subcommand to run. This can be:\n' + '\n'.join(
                    ['\t%(key)s\t%(help)s' % {'key': key, 'help': value['help']} for key, value in commands.items()]
                )
            )

        # run the appropriate subcommand
        commands[args[0]]['method']()

    def email_checker_task(self):
        """
        Executes the IPEMailChecker tasks (that is a periodic task!)
        """
        IPEMailChecker().delay()

    def unify_ips(self):
        """
        Runs the IP unification.
        """
        IP.unify_ips()

    def location_replacement(self):
        UpdateHtaccessLocationsTask.delay()

    def update_locations(self):
        UpdateLocationsIfNecessaryTask.delay()
