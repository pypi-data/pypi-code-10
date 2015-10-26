"""Runserver command with bysnc"""
from optparse import make_option
# try:
#     from urllib.request import urlopen
# except ImportError:  # Python 2 fall back
#     from urllib2 import urlopen

from django.conf import settings
from django.core.management.color import color_style
import os

if 'django.contrib.staticfiles' in settings.INSTALLED_APPS:
    from django.contrib.staticfiles.management.commands.runserver import \
        Command as RunserverCommand
else:
    from django.core.management.commands.runserver import \
        Command as RunserverCommand


class Command(RunserverCommand):
    """
    Command for running the development server with bysnc.
    """
    if callable(getattr(RunserverCommand, 'add_arguments', None)):
        def add_arguments(self, parser):
            super(Command, self).add_arguments(parser)
            parser.add_argument('--nobsync', action='store_false',
                                dest='use_bysnc', default=True,
                                help='Tells Django to NOT use bysnc.')
            parser.add_argument('--bysnc-port', action='store',
                                dest='bysnc_port', default='3000',
                                help='Port where bysnc listen.')
    else:
        option_list = RunserverCommand.option_list + (
                make_option('--nobsync', action='store_false',
                            dest='use_bysnc', default=True,
                            help='Tells Django to NOT use bysnc.'),
                make_option('--bysnc-port', action='store',
                            dest='bysnc_port', default='',
                            help='Port where bysnc listen.'),
        )

    help = 'Starts a lightweight Web server for development with browser-sync reload.'

    def message(self, message, verbosity=1, style=None):
        if verbosity:
            if style:
                message = style(message)
            self.stdout.write(message)

    def bysnc_request(self, **options):
        """
        Performs the bysnc request.
        """
        style = color_style()
        verbosity = int(options['verbosity'])

        bysnc_port = options['bysnc_port']

        if options['bysnc_port']:
            sub_cmd = " --port {}".format(bysnc_port)
        else:
            sub_cmd = ""

        cmd = "browser-sync reload{}".format(sub_cmd)

        # host = 'localhost:%s' % options['bysnc_port']
        try:
            os.system(cmd)
            #urlopen('http://%s/changed?files=.' % host)
            self.message('bysnc request emitted. cmd ={}\n'.format(cmd),
                         verbosity, style.HTTP_INFO)
        except IOError:
            pass

    def get_handler(self, *args, **options):
        """
        Entry point to plug the bysnc feature.
        """
        handler = super(Command, self).get_handler(*args, **options)
        if options['use_bysnc']:
            self.bysnc_request(**options)
        return handler
