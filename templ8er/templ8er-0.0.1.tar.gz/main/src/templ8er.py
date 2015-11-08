#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import click

from modules.python import T8Python
from modules.ruby import T8Ruby
# from modules.docker import T8Docker

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
CWD = os.getcwd()

# Main command
@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--name', default='from_t8er', type=str, help='Name of generating script without extension. [default="from_t8er"]')
@click.pass_context
def t8er(ctx, name):
    ctx.obj['NAME'] = name

## 'Python' subcommand
@t8er.group(context_settings=CONTEXT_SETTINGS)
@click.option('--name', default='from_t8er', type=str, help='Name of generating script without extension. [default="from_t8er"]')
@click.pass_context
def python(ctx, name):
    ctx.obj['NAME'] = name

### 'Simple Python Script' subsubcommand
@python.command(context_settings=CONTEXT_SETTINGS)
@click.option('--name', default='from_t8er', type=str, help='Name of generating script without extension. [default="from_t8er"]')
@click.option('--packages', default=None, type=str, help='Name of a file that lists required packages as plain text. [default=None]')
@click.pass_context
def simple(ctx, name, packages):
    click.echo('Simple python script')
    ctx.obj['NAME'] = name
    ctx.obj['PACKAGES'] = packages
    T8Python(CWD).simple_python_script(name, packages)

python.add_command(simple)

## 'Ruby' subcommand
@t8er.group(context_settings=CONTEXT_SETTINGS)
@click.option('--name', default='from_t8er', type=str, help='Name of generating script without extension. [default="from_t8er"]')
@click.pass_context
def ruby(ctx, name):
    ctx.obj['NAME'] = name

### 'Simple Ruby Script' subsubcommand
@ruby.command(context_settings=CONTEXT_SETTINGS)
@click.option('--name', default='from_t8er', type=str, help='Name of generating script without extension. [default="from_t8er"]')
@click.option('--packages', default=None, type=str, help='Name of a file that lists required packages as plain text. [default=None]')
@click.pass_context
def simple(ctx, name, packages):
    click.echo('Simple ruby script')
    ctx.obj['NAME'] = name
    ctx.obj['PACKAGES'] = packages
    T8Ruby(CWD).simple_ruby_script(name, packages)

ruby.add_command(simple)

#
def main():
    t8er(obj={})

#
if __name__=="__main__":
    main()
