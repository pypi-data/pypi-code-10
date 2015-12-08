import os
import shlex

from six.moves import input

from django import setup
from django.core import management


def start_celery():
    setup()
    management.call_command('celeryd')

def start_celerybeat():
    setup()
    management.call_command('celerybeat', pidfile=None)

def run_migrations():
    setup()
    args = shlex.split(os.getenv('MIGRATE_ARGS', ''))
    management.call_command('migrate', *args)

    if os.getenv('SLEEP_FOREVER') == 'true':
        input()
