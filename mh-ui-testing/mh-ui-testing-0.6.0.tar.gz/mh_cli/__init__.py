__version__ = '0.6.0'

import click
click.disable_unicode_literals_warning = True

@click.group()
def cli():
    pass

from gi import gi
from inbox import inbox
from tasks import *
from series import series
