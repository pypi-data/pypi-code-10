import sys
from django.core.management import BaseCommand
from sensei2.sensei.sensei_room import Sensei
from termcolor import cprint


class Command(BaseCommand):
    def handle(self, *args, **options):
        group = sys.argv[2]  # group of SENSEI_RULES to execute
        sensei = Sensei(group)
        try:
            sensei.teach()
        except Exception, e:
            cprint("\n\nSensei stopped. Need more meditate", "red")
