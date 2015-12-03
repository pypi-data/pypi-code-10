#!/usr/bin/env python
import os
import shlex
import sys

import yaml


def cli():
    command_name = sys.argv[1]
    extra_args = sys.argv[2:]

    cwd_path = os.path.join(os.getcwd(), 'Procfile')
    env_path = os.environ.get('PROCFILE_PATH')

    if os.path.exists(cwd_path):
        procfile_path = cwd_path
    elif env_path and os.path.exists(env_path):
        procfile_path = env_path
    else:
        sys.exit('no Procfile path defined')

    with open(procfile_path) as fh:
        command = yaml.load(fh)[command_name]

    if isinstance(command, basestring):
        command = shlex.split(command)

    os.execvpe(command[0], command + extra_args, os.environ)


if __name__ == "__main__":
    cli()
