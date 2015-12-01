import shlex

from .ast import Aliasfile, CommandSpec


def parse_configuration(config):
    return Aliasfile(
        commands={
            name: _parse_command_spec(name, spec)
            for name, spec in config.get('commands', {}).items()
        },
        env=config.get('env'))


def _parse_command_spec(name, spec):
    if not isinstance(spec, dict):
        spec = {'command': spec}

    return CommandSpec(
        name,
        command=_parse_command_line(spec.get('command')),
        append_args=spec.get('append_args', True),
        env=spec.get('env'))


def _parse_command_line(cmd):
    if cmd is None:
        return []

    if isinstance(cmd, bytes):
        cmd = cmd.decode()

    if isinstance(cmd, str):
        return shlex.split(cmd)

    return [str(x) for x in cmd]
