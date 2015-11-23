import re
import os
import shlex

import click
import yaml


def list_commands(config):
    click.echo('Available commands:')
    for name, cmd in sorted(config.get('commands', {}).items()):
        click.echo('    \x1b[1m{}\x1b[0m'.format(name))


def _print_command(args):
    click.echo('\x1b[1m>\x1b[0m \x1b[34m{}\x1b[0m'
               .format(_format_command(args)))


def _format_command(args):
    return ' '.join(_escape_argument(a) for a in args)


def _escape_argument(text):
    re_no_need_escaping = re.compile(r'^[0-9a-zA-Z_\.-]+$')
    if re_no_need_escaping.match(text):
        return text

    # Replace single backslash with double
    text = text.replace('\\', '\\\\')

    text = text.replace('\n', '\\n')
    text = text.replace('\r', '\\r')
    text = text.replace('"', '\\"')

    return '"{}"'.format(text)


class Command:
    def __init__(self, name, spec):
        self.name = name

        self.raw_command = []
        self.raw_env = {}
        self.raw_vars = {}

        if isinstance(spec, dict):
            self.raw_command = shlex.split(spec['command'])
            self.raw_env = spec.get('env') or {}
            self.raw_vars = spec.get('vars') or {}

        elif isinstance(spec, (str, bytes)):
            self.raw_command = shlex.split(spec)

        else:
            raise TypeError('Unsupported command spec type')

    def get_command(self, args):
        return [self._substitute(arg, args)
                for arg in self.raw_command] + args

    def get_env(self, args):
        return {key: self._substitute(val, args)
                for key, val in self.raw_env.items()}

    def get_vars(self, args):
        return {key: self._substitute(val, args, with_vars=False)
                for key, val in self.raw_vars.items()}

    def run(self, args):
        cmd = self.get_command(args)
        env = os.environ.copy()
        env.update(self.get_env(args))
        _print_command(cmd)

        os.execvpe(cmd[0], cmd, env)

    def _substitute(self, s, args, with_vars=True):
        context = {
            'env': os.environ,
            'args': args,
        }
        if with_vars:
            context['vars'] = self.get_vars(args)
        return s.format(*args, **context)


@click.command()
@click.option('--config', 'config_filename', default='.aliases')
@click.argument('args', nargs=-1)
def main(config_filename, args):
    with open(config_filename, 'r') as fp:
        config = yaml.load(fp)

    if len(args) < 1:
        return list_commands(config)

    cmd_name, *pos_args = args

    spec = config['commands'][cmd_name]
    cmd = Command(cmd_name, spec)
    cmd.run(pos_args)
