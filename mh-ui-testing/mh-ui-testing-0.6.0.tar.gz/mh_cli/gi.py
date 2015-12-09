import click
from mh_cli import cli

from os.path import dirname
from fabric.api import local, lcd


@cli.group()
def gi():
    """Do stuff with Ghost Inspector tests"""

@gi.command(name='list', context_settings=dict(ignore_unknown_options=True))
@click.argument('gi_args', nargs=-1, type=click.UNPROCESSED)
def gi_list(gi_args):
    """Collect and list available tests"""
    with(lcd(dirname(dirname(__file__)))):
        local("py.test --verbose --collect-only %s" % " ".join(gi_args))


@gi.command(name='exec', context_settings=dict(ignore_unknown_options=True))
@click.argument('gi_args', nargs=-1, type=click.UNPROCESSED)
def gi_exec(gi_args):
    """Execute tests"""
    with(lcd(dirname(dirname(__file__)))):
        local("py.test --verbose %s" % " ".join(gi_args))
