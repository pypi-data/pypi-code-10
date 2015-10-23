# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from django.core.management.base import BaseCommand, CommandError
from ...package import run_check
import sys
import traceback


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            run_check()
            sys.exit(0)
        except Exception as e:
            traceback.print_exc()
            sys.exit(1)
