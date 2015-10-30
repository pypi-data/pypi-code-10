from imp import reload

from django.db import connection
from django.core.management import call_command
from django.test import TestCase

from parent_swap import dependencies, fields, swap
from parent_swap.tests.simple_app import models


def drop_table(table_name):
    cursor = connection.cursor()
    cursor.execute(
        '''DROP TABLE {};'''.format(table_name)
    )
    cursor.close()


class AppReloadTestCase(TestCase):
    """
    Reloads the relevant python modules to test the swappable models in isolation.
    """
    def setUp(self):
        reload(swap)
        reload(fields)
        reload(dependencies)
        reload(models)
        super(AppReloadTestCase, self).setUp()

        # We're gonna have to re-run migrations since we want to start in a new environment.
        if getattr(self, 'drop_table', True):
            drop_table(models.SimpleObject._meta.db_table)
        if getattr(self, 'migrate', True):
            call_command('migrate', verbosity=0)
