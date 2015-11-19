from .command import Command
import sys
import re
import subprocess


class SubstituteKeywords(Command):

    def _execute(self):
        substitutions = {
            'version': subprocess.check_output(
                ['git', 'describe', '--always'],
                stderr=subprocess.STDOUT),
            'date': subprocess.check_output(
                ['git', 'log', '--pretty=format:"%ad"', '-1']
                stderr=subprocess.STDOUT),
        }
        for key, value in substitutions.items():
            value = re.sub(r'[\n\r\t"\"]', '', value)

        for line in sys.stdin:
            for key, value in substitutions.items():
                rexp = '%s:' % key
                line = re.sub(rexp, '%s: %s' % (key, value), line)
            sys.stdout.write(line)


class CleanKeywords(Command):

    def _execute(self):
        substitutions = {
            'version': None,
            'date': None,
        }

        for line in sys.stdin:
            for key in substitutions:
                rexp = '%s:.*' % key
                line = re.sub(rexp, '%s:' % key, line)
            sys.stdout.write(line)
