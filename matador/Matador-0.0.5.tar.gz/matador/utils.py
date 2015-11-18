#!/usr/bin/env python
import os
import subprocess
import yaml


def working_folder(project, environment):
    working_path = os.path.expanduser(
        '~/.matador/%s/%s' % (project, environment))
    os.makedirs(working_path, exist_ok=True)
    return working_path


def is_git_repository(path='.'):
    return subprocess.run(
        ['git', '-C', path, 'status'],
        stderr=subprocess.STDOUT,
        stdout=open(os.devnull, 'w')) == 0


def project_folder(path='.'):
    git_output = subprocess.check_output(
        ['git', '-C', path, 'rev-parse', '--show-toplevel'],
        stderr=subprocess.STDOUT)
    return git_output.decode('utf-8').strip('\n')


def project():
    return os.path.basename(project_folder())


def environments():
    return yaml.load(os.path.join(
        project_folder(), 'config', 'environments.yml'))
