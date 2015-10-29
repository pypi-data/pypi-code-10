"""Do the checks and tasks that have to happen before doing a release.
"""
from __future__ import unicode_literals

import datetime
import logging
import six
import sys

from zest.releaser import baserelease
from zest.releaser import utils
from zest.releaser.utils import execute_command
from zest.releaser.utils import read_text_file
from zest.releaser.utils import write_text_file
from zest.releaser.postrelease import NOTHING_CHANGED_YET

logger = logging.getLogger(__name__)

TODAY = datetime.datetime.today().strftime('%Y-%m-%d')
HISTORY_HEADER = '%(new_version)s (%(today)s)'
PRERELEASE_COMMIT_MSG = 'Preparing release %(new_version)s'

DATA = {
    # Documentation for self.data.  You get runtime warnings when something is
    # in self.data that is not in this list.  Embarrasment-driven
    # documentation!
    'workingdir': 'Original working directory',
    'reporoot': 'Root of the version control repository',
    'name': 'Name of the project being released',
    'today': 'Date string used in history header',
    'new_version': 'New version (so 1.0 instead of 1.0dev)',
    'history_file': 'Filename of history/changelog file (when found)',
    'history_last_release': (
        'Full text of all history entries of the current release'),
    'history_lines': 'List with all history file lines (when found)',
    'history_encoding': 'The detected encoding of the history file',
    'history_insert_line_here': (
        'Line number where an extra changelog entry can be inserted.'),
    'nothing_changed_yet': (
        'First line in new changelog section, '
        'warn when this is still in there before releasing'),
    'required_changelog_text': (
        'Text that must be present in the changelog. Can be a string or a '
        'list, for example ["New:", "Fixes:"]. For a list, only one of them '
        'needs to be present.'),
    'original_version': 'Version before prereleasing (e.g. 1.0dev)',
    'commit_msg': 'Message template used when committing',
    'history_header': 'Header template used for 1st history header',
}


class Prereleaser(baserelease.Basereleaser):
    """Prepare release, ready for making a tag and an sdist.

    self.data holds data that can optionally be changed by plugins.

    """

    def __init__(self, vcs=None):
        baserelease.Basereleaser.__init__(self, vcs=vcs)
        # Prepare some defaults for potential overriding.
        self.data.update(dict(
            today=datetime.datetime.today().strftime('%Y-%m-%d'),
            history_header=HISTORY_HEADER,
            commit_msg=PRERELEASE_COMMIT_MSG,
            nothing_changed_yet=NOTHING_CHANGED_YET,
        ))

    def prepare(self):
        """Prepare self.data by asking about new version etc."""
        if not utils.sanity_check(self.vcs):
            logger.critical("Sanity check failed.")
            sys.exit(1)
        if not utils.check_recommended_files(self.data, self.vcs):
            logger.debug("Recommended files check failed.")
            sys.exit(1)
        self._grab_version()
        self._grab_history()

    def execute(self):
        """Make the changes and offer a commit"""
        self._write_version()
        self._write_history()
        self._diff_and_commit()

    def _grab_version(self):
        """Set the version to a non-development version."""
        original_version = self.vcs.version
        logger.debug("Extracted version: %s", original_version)
        if original_version is None:
            logger.critical('No version found.')
            sys.exit(1)
        suggestion = utils.cleanup_version(original_version)
        new_version = utils.ask_version("Enter version", default=suggestion)
        if not new_version:
            new_version = suggestion
        self.data['original_version'] = original_version
        self.data['new_version'] = new_version

    def _write_version(self):
        if self.data['new_version'] != self.data['original_version']:
            # self.vcs.version writes it to the file it got the version from.
            self.vcs.version = self.data['new_version']
            logger.info("Changed version from %s to %s",
                        self.data['original_version'],
                        self.data['new_version'])

    def _grab_history(self):
        """Calculate the needed history/changelog changes

        Every history heading looks like '1.0 b4 (1972-12-25)'. Extract them,
        check if the first one matches the version and whether it has a the
        current date.
        """
        default_location = None
        config = self.setup_cfg.config
        if config and config.has_option('zest.releaser', 'history_file'):
            default_location = config.get('zest.releaser', 'history_file')
        history_file = self.vcs.history_file(location=default_location)
        if not history_file:
            logger.warn("No history file found")
            self.data['history_lines'] = None
            self.data['history_file'] = None
            self.data['history_encoding'] = None
            return
        logger.debug("Checking %s", history_file)
        history_lines, history_encoding = read_text_file(history_file)
        history_lines = history_lines.split('\n')
        headings = utils.extract_headings_from_history(history_lines)
        if not len(headings):
            logger.error("No detectable version heading in the history "
                         "file %s", history_file)
            sys.exit(1)
        good_heading = self.data['history_header'] % self.data
        # ^^^ history_header is a string with %(abc)s replacements.
        line = headings[0]['line']
        previous = history_lines[line]
        history_lines[line] = good_heading
        logger.debug("Set heading from %r to %r.", previous, good_heading)
        history_lines[line + 1] = utils.fix_rst_heading(
            heading=good_heading,
            below=history_lines[line + 1])
        logger.debug("Set line below heading to %r",
                     history_lines[line + 1])
        self.data['history_lines'] = history_lines
        self.data['history_file'] = history_file
        self.data['history_encoding'] = history_encoding

        # Look for 'Nothing changed yet' under the latest header.  Not
        # nice if this text ends up in the changelog.  Did nothing happen?
        start = headings[0]['line']
        if len(headings) > 1:
            end = headings[1]['line']
        else:
            end = len(history_lines)
        history_last_release = '\n'.join(history_lines[start:end])
        self.data['history_last_release'] = history_last_release
        if self.data['nothing_changed_yet'] in history_last_release:
            # We want quotes around the text, but also want to avoid printing
            # text with a u'unicode marker' in front...
            pretty_nothing_changed = '"{}"'.format(
                self.data['nothing_changed_yet'])
            if not utils.ask(
                    "WARNING: Changelog contains {}. Are you sure you "
                    "want to release?".format(pretty_nothing_changed),
                    default=False):
                logger.info("You can use the 'lasttaglog' command to "
                            "see the commits since the last tag.")
                sys.exit(1)

        # Look for required text under the latest header.  This can be a list,
        # in which case only one item needs to be there.
        required = self.data.get('required_changelog_text')
        if required:
            if isinstance(required, six.string_types):
                required = [required]
            found = False
            for text in required:
                if text in history_last_release:
                    found = True
                    break
            if not found:
                pretty_required = '"{}"'.format('", "'.join(required))
                if not utils.ask(
                        "WARNING: Changelog should contain at least one of "
                        "these required strings: {}. Are you sure you "
                        "want to release?".format(pretty_required),
                        default=False):
                    sys.exit(1)

        # Add line number where an extra changelog entry can be inserted.  Can
        # be useful for entry points.  'start' is the header, +1 is the
        # underline, +2 is probably an empty line, so then we should take +3.
        # Or rather: the first non-empty line.
        insert = start + 2
        while insert < end:
            if history_lines[insert].strip():
                break
            insert += 1
        self.data['history_insert_line_here'] = insert

    def _write_history(self):
        """Write previously-calculated history lines back to the file"""
        if self.data['history_file'] is None:
            return
        contents = '\n'.join(self.data['history_lines'])
        history = self.data['history_file']
        write_text_file(
            history, contents, encoding=self.data['history_encoding'])
        logger.info("History file %s updated.", history)

    def _diff_and_commit(self):
        diff_cmd = self.vcs.cmd_diff()
        diff = execute_command(diff_cmd)
        if sys.version.startswith('2.6.2'):
            # python2.6.2 bug... http://bugs.python.org/issue5170 This is the
            # spot it can surface as we show a part of the changelog which can
            # contain every kind of character.  The rest is mostly ascii.
            print("Diff results:")
            print(diff)
        else:
            # Common case
            logger.info("The '%s':\n\n%s\n", diff_cmd, diff)
        if utils.ask("OK to commit this"):
            msg = self.data['commit_msg'] % self.data
            msg = self.update_commit_message(msg)
            commit_cmd = self.vcs.cmd_commit(msg)
            commit = execute_command(commit_cmd)
            logger.info(commit)


def datacheck(data):
    """Entrypoint: ensure that the data dict is fully documented"""
    utils.is_data_documented(data, documentation=DATA)


def main():
    utils.parse_options()
    utils.configure_logging()
    prereleaser = Prereleaser()
    prereleaser.run()
