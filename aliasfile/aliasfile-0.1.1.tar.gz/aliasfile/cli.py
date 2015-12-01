import os

import click
import yaml

from .parse import parse_configuration
from .runner import run_command
from .utils import format_command


def list_commands(config):
    click.echo('Available commands\n'
               '==================')
    for name, cmd in sorted(config.commands.items()):
        click.echo(
            '    \x1b[1m{}\x1b[0m'
            ' \x1b[34m{}\x1b[0m'
            .format(name, format_command(cmd.command)))


@click.command(context_settings=dict(allow_interspersed_args=False))
@click.option('--config', 'config_filename', default='.aliases')
@click.option('--list', 'action_list', is_flag=True, is_eager=True)
@click.argument('args', nargs=-1)
def main(config_filename, args, action_list=False):

    with open(config_filename, 'r') as fp:
        raw_config = yaml.load(fp)
    config = parse_configuration(raw_config)

    if action_list or len(args) < 1:
        return list_commands(config)

    cmd_name, *pos_args = args

    run_command(config, cmd_name, pos_args, env=os.environ)
