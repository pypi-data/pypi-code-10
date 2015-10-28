#!/usr/bin/env python
"""Entry point for Django DDP test project."""
import os
import sys


if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'dddp.test.test_project.settings'

    from dddp import greenify
    greenify()

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
