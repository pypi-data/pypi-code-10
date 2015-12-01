import os

import click

from .utils import format_command, format_envvar


def run_command(config, name, args=None, env=None):
    if args is None:
        args = []

    if env is None:
        env = os.environ

    env = env.copy()  # We're going to update it

    cmd_spec = config.commands[name]

    extra_env = {}
    extra_env.update(config.env)
    extra_env.update(cmd_spec.env)
    env.update(extra_env)

    run_args = []
    run_args.extend(cmd_spec.command)

    run_args = _apply_replacements_list(run_args, {'args': args, 'env': env})

    if cmd_spec.append_args:
        run_args.extend(args)

    click.echo('\x1b[1m>\x1b[0m {}'.format(format_command(run_args)))
    for key, value in sorted(extra_env.items()):
        click.echo('  {}'.format(format_envvar(key, value)))

    os.execvpe(run_args[0], run_args, env)


def _apply_replacements(text, context):
    return text.format(*context['args'], **context)


def _apply_replacements_dict(obj, context):
    return {key: _apply_replacements(val, context)
            for key, val in obj.items()}


def _apply_replacements_list(obj, context):
    return [_apply_replacements(x, context) for x in obj]
