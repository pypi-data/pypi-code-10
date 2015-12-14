import logging
import subprocess
import re


def substitute_keywords(text, repo_folder, commit):
    substitutions = {
        'version': commit,
        'date': subprocess.check_output(
            ['git', '-C', repo_folder, 'show', '-s', '--format=%ci',
            '%s^{commit}' % commit],
            stderr=subprocess.STDOUT).decode().strip('\n'),
    }
    new_text = ''
    for line in text.splitlines(keepends=True):
        for key, value in substitutions.items():
            rexp = '%s:.*' % key
            line = re.sub(rexp, '%s: %s' % (key, value), line)
        new_text += line
    return new_text


class DeploymentCommand(object):

    def __init__(self, *args):
        self._logger = logging.getLogger(__name__)
        self.args = args
        self._execute()

    def _execute(self):
        raise NotImplementedError
