import os
import sys

import django
from django.conf import settings
from django.test.runner import DiscoverRunner

DJANGO_DEBUG = os.environ.get('DJANGO_DEBUG', 1)
SWAP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# DEFAULT_BASE_CLASS = 'parent_swap.tests.parent_app.models.SimpleParent'

EXTERNAL_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
]

INTERNAL_APPS = [
    'parent_swap.tests.parent_app',
    'parent_swap.tests.simple_app'
]

INSTALLED_APPS = tuple(EXTERNAL_APPS + INTERNAL_APPS)

MIDDLEWARE_CLASSES = tuple()

SECRET_KEY = '12345'

if not settings.configured:
    settings.configure(
        # DEFAULT_BASE_CLASS=DEFAULT_BASE_CLASS,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:"
            }
        },
        INSTALLED_APPS=INSTALLED_APPS,
        ROOT_URLCONF='parent_swap.tests.urls',
        TEMPLATE_DIRS=(
            os.path.join(os.path.dirname(__file__), '../templates'),
        ),
    )


def main():
    if django.VERSION >= (1, 7):
        django.setup()
    runner = DiscoverRunner(failfast=True, verbosity=int(DJANGO_DEBUG))
    failures = runner.run_tests(['parent_swap'], interactive=True)
    sys.exit(failures)

if __name__ == '__main__':
    main()
