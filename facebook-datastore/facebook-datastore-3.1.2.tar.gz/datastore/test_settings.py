from datastore.settings import *
from os import path
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

PROJECT_ROOT = path.abspath(path.dirname(__file__))

STATIC_ROOT = '/tmp/datastore-jenkins-test/static/'
STATIC_URL = '/static/'
MEDIA_ROOT = '/tmp/datastore-jenkins-test/media/'
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = urljoin(STATIC_URL, 'admin/')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'datastore-test-database',
    }
}

FACEBOOK_APP_ID = 123
FACEBOOK_APP_SECRET = '123'

INSTALLED_APPS += ('django_jenkins', )

JENKINS_TASKS = (
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
)

SITE_ID = 1
