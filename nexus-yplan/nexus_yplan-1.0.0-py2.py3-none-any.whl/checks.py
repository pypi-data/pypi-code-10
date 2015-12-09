import django
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from nexus.compat import Error, Tags, register


def register_checks():
    register(Tags.compatibility)(check_requirements)


def check_requirements(app_configs, **kwargs):
    errors = []

    if getattr(settings, 'NEXUS_SKIP_INSTALLED_APPS_REQUIREMENTS', False):
        reqs = ()
    else:
        reqs = ('django.contrib.auth', 'django.contrib.sessions')

    for req in reqs:
        if req not in settings.INSTALLED_APPS:
            errors.append(Error(
                "Nexus depends on '{}'".format(req),
                id='nexus.E001',
                hint="Add '{}' to INSTALLED_APPS or set NEXUS_SKIP_INSTALLED_APPS_REQUIREMENTS = True.".format(req)
            ))

    return errors


def pre_checks_requirements():
    # Used in models.py to raise an error for django versions that can't use the above check
    if django.VERSION >= (1, 7):
        return

    errors = check_requirements([])

    if not len(errors):
        return

    message = " ".join(error.msg + " " + error.hint for error in errors)
    raise ImproperlyConfigured(message)
