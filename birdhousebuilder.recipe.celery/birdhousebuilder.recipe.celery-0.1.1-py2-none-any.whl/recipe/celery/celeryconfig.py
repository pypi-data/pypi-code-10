# celery scheduler config
# http://celery.readthedocs.org/en/latest/configuration.html

% if 'broker-url' in options:
# Broker settings.
BROKER_URL = '${options["broker-url"]}'
% endif

% if 'celery-result-backend' in options:
# Backend to store task state and results.
CELERY_RESULT_BACKEND = '${options["celery-result-backend"]}'
% endif

% if 'celery-imports' in options:
# List of modules to import when celery starts.
CELERY_IMPORTS = ${repr(tuple(options["celery-imports"].split()))}
% endif

% if 'celeryd-concurrency' in options:
# The number of concurrent worker processes/threads/green threads executing tasks.
CELERYD_CONCURRENCY = ${options["celeryd-concurrency"]}
% endif



