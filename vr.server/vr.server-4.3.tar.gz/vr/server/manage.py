#!/usr/bin/env python
import os
import sys


# Ideally, the value of DJANGO_SETTINGS_MODULE would be "vr.server.settings".
# Unfortunately, that value doesn't work with the standard ``manage.py`` file
# provided by Django 1.4+ (this file), due to ``vr`` being a namespaced
# Python package. Therefore, the following ``sys.path`` trick allows us to use
# "server.settings" as the value of the Django settings module.
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
)


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
