"""Watch for changes in a collection of source files. If changes, run
the specified test runner (nosetests, by default).
"""
from argparse import ArgumentParser
try:
    import configparser as ConfigParser
except ImportError:
    import ConfigParser
import glob
import os
import stat
import subprocess
import sys
import time


class Nosy(object):
    """Watch for changes in all source files. If changes, run the
    specified test runner (nosetests, by default).
    """
    def __init__(self):
        """Return an instance with the default configuration, and a
        command line parser.
        """
        self.config = ConfigParser.SafeConfigParser()
        self.config.add_section('nosy')
        self.config.set('nosy', 'test_runner', 'nosetests')
        self.config.set('nosy', 'base_path', '.')
        self.config.set('nosy', 'glob_patterns', '')
        self.config.set('nosy', 'exclude_patterns', '')
        self.config.set('nosy', 'extra_paths', '')
        self.config.set('nosy', 'options',  '')
        self.config.set('nosy', 'tests', '')
        # paths config retained for backward compatibility; use
        # extra_paths for any files or paths that aren't easily
        # included via base_path, glob_patterns, and exclude_patterns
        self.config.set('nosy', 'paths', '*.py')
        self._build_cmdline_parser()

    def _build_cmdline_parser(self):
        self.parser = ArgumentParser(
            description='Automatically run a command (nosetest, by default) '
                        'whenever source files change.')
        self.parser.add_argument(
            '-c', '--config', dest='config_file', default='setup.cfg',
            help='configuration file path and name; defaults to %(default)s')

    def parse_cmdline(self):
        """Parse the command line and set the config_file attribute.
        """
        args = self.parser.parse_args()
        self.config_file = args.config_file

    def _read_config(self):
        try:
            self.config.readfp(open(self.config_file, 'rt'))
        except IOError:
            msg = sys.exc_info()[1]
            self.parser.error("can't read config file:\n %s" % msg)
        self.test_runner = self.config.get('nosy', 'test_runner')
        self.base_path = self.config.get('nosy', 'base_path')
        self.glob_patterns = self.config.get(
            'nosy', 'glob_patterns').split()
        self.exclude_patterns = self.config.get(
            'nosy', 'exclude_patterns').split()
        self.extra_paths = self.config.get('nosy', 'extra_paths').split()
        self.cmd_opts = self.config.get('nosy', 'options')
        self.cmd_args = self.config.get('nosy', 'tests')
        # paths config retained for backward compatibility; use
        # extra_paths for any files or paths that aren't easily
        # included via base_path, glob_patterns, and
        # exclude_patterns
        self.paths = self.config.get('nosy', 'paths').split()

    def _calc_extra_paths_checksum(self):
        """Return the checksum for the files given by the extra paths
        pattern(s).

        self.paths is included for backward compatibility.
        """
        checksum = 0
        for path in self.extra_paths + self.paths:
            for file_path in glob.iglob(path):
                stats = os.stat(file_path)
                checksum += stats[stat.ST_SIZE] + stats[stat.ST_MTIME]
        return checksum

    def _calc_exclusions(self, root):
        """Return a set of file paths to be excluded from the checksum
        calculation.
        """
        exclusions = set()
        for pattern in self.exclude_patterns:
            for file_path in glob.iglob(os.path.join(root, pattern)):
                exclusions.add(file_path)
        return exclusions

    def _calc_dir_checksum(self, exclusions, root):
        """Return the checksum for the monitored files in the
        specified directory tree.
        """
        checksum = 0
        for pattern in self.glob_patterns:
            for file_path in glob.iglob(os.path.join(root, pattern)):
                if file_path not in exclusions:
                    stats = os.stat(file_path)
                    checksum += stats[stat.ST_SIZE] + stats[stat.ST_MTIME]
        return checksum

    def _checksum(self):
        """Return a checksum which indicates if any files in the paths
        list have changed.
        """
        checksum = self._calc_extra_paths_checksum()
        for root, dirs, files in os.walk(self.base_path):
            exclusions = self._calc_exclusions(root)
            checksum += self._calc_dir_checksum(exclusions, root)
        return checksum

    def run(self):
        """Run specified test runner (default nosetests) whenever the
        source files (default ./*.py) change.

        Re-read the configuration before each run so that options and
        arguments may be changed.
        """
        checksum = 0
        self._read_config()
        while True:
            if self._checksum() != checksum:
                self._read_config()
                checksum = self._checksum()
                cmd = (self.test_runner.split() if ' ' in self.test_runner
                       else [self.test_runner])
                try:
                    subprocess.call(
                        cmd
                        + self.cmd_opts.replace('\\\n', '').split()
                        + self.cmd_args.replace('\\\n', '').split())
                except OSError:
                    msg = sys.exc_info()[1]
                    sys.stderr.write('Command error: %s: %s\n' % (msg, cmd))
                    sys.exit(2)
            time.sleep(1)


def main():
    nosy = Nosy()
    nosy.parse_cmdline()
    try:
        nosy.run()
    except KeyboardInterrupt:
        sys.exit(130)
    except SystemExit:
        sys.exit(0)


if __name__ == '__main__':
    main()
