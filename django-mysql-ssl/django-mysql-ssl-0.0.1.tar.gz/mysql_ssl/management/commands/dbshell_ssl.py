from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.db import connections, DEFAULT_DB_ALIAS
from mysql_ssl.backends.mysql.client import MysqlSslClient

class Command(BaseCommand):
    help = ("Runs the command-line client for specified database, or the "
        "default database if none is provided.")

    option_list = BaseCommand.option_list + (
        make_option('--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS, help='Nominates a database onto which to '
                'open a shell.  Defaults to the "default" database.'),
    )

    requires_model_validation = False

    def handle(self, **options):
        ssl_client = MysqlSslClient()
        connection = connections[options.get('database')]
        try:
            ssl_client.runshell(connection)
        except OSError:
            # Note that we're assuming OSError means that the client program
            # isn't installed. There's a possibility OSError would be raised
            # for some other reason, in which case this error message would be
            # inaccurate. Still, this message catches the common case.
            raise CommandError('You appear not to have the %r program installed or on your path.' % \
                connection.client.executable_name)
