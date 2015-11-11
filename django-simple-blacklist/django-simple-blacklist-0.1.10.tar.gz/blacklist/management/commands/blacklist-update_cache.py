# coding=utf-8
# django-simple-blacklist 11/9/15 2:02 PM by mnach #
import logging
from django.core.management import BaseCommand
from blacklist import models
import sys
from django.core.cache import cache

log = logging.getLogger('remove_request_logs')


class Command(BaseCommand):
    help = 'Update database queries cache'

    def handle(self, *args, **opts):
        if not models._cached_queries:
            print("You don't cache database queries. Please set CACHED_BLOCKING_RULES to True in your settings.py")
            sys.exit(1)

        all_rules = tuple(models.BlockRules.objects.defer('created', 'updated').all())
        cache.set('all-block-rules', all_rules)
        print("Cache updated successfully. Blocking rules count {0}".format(len(all_rules)))
