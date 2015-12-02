import os
import shlex

# Make sure Django settings are loaded.
os.environ['DJANGO_SETTINGS_MODULE'] = 'vr.server.settings'

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
        raw_input()
