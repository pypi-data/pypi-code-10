#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from .packages import click
from . import commands


class LazyCLI(click.MultiCommand):
    '''Lazily imports interfaces from wanderer.commands package.'''

    def list_commands(self, ctx):
        cmds = [cmd for cmd in dir(commands) if not cmd.startswith('__')]
        return sorted(cmds)

    def get_command(self, ctx, name):
        cmd_module = getattr(commands, name)
        return cmd_module.cli


@click.group(cls=LazyCLI)
@click.pass_context
def cli(ctx):
    '''Wanderer Command Line Tools'''
    pass


if __name__ == '__main__':
    cli()
