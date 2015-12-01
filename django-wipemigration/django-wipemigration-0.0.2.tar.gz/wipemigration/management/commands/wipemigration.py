from django.core.management.base import BaseCommand
from django.db.migrations.recorder import MigrationRecorder


class Command(BaseCommand):
    help = 'Wipe django migrations.'

    def add_arguments(self, parser):
        parser.add_argument('args', metavar='app_label', nargs='*',
            help='Specify the app label(s) to wipe migrations for.')

    def handle(self, *app_labels, **options):
        Migration = MigrationRecorder(None).Migration
        for app_label in app_labels:
            count = Migration.objects.filter(app=app_label).count()
            ans = input(
                'Are you sure you want to delete all (%s) migrations '
                'for %s? [Y/n] ' % (count, app_label)
            )
            if ans == 'Y':
                Migration.objects.filter(app=app_label).delete()
                print('Done.')
            else:
                print('No action.')
