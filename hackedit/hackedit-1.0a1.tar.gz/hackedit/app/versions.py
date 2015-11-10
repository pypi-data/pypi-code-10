"""
Provides some functions to retrieve various version informations.
"""
import logging
import subprocess

from hackedit import __version__


def _logger():
    return logging.getLogger(__name__)


def get_vcs_revision():
    """
    Gets the vcs revision (git branch + commit).
    """
    def get_git_revision_hash():
        return subprocess.check_output(
            ['git', 'rev-parse', '--short', 'HEAD']).decode('utf-8').replace(
            '\n', '')

    def get_git_branch_name():
        output = subprocess.check_output(['git', 'branch']).decode('utf-8')
        for l in output.splitlines():
            if l.startswith('*'):
                return l.replace('*', '').replace(' ', '')
        return 'master'

    try:
        return '%s@%s' % (get_git_revision_hash(), get_git_branch_name())
    except (OSError, subprocess.CalledProcessError):
        _logger().warning('Failed to get vcs revision')
        return ''


def get_versions():
    """ Get version information for components used by HackEdit """
    import locale
    import sys
    import platform

    from PyQt5.QtCore import QT_VERSION_STR
    from PyQt5.QtCore import PYQT_VERSION_STR
    from pyqode.core import __version__ as corev

    from hackedit.api import system

    if system.LINUX:
        distro = ' '.join(platform.linux_distribution())
        if not distro.strip():
            try:
                out = str(subprocess.check_output(['lsb_release', '-i']),
                          locale.getpreferredencoding())
            except OSError:
                distro = ':distribution not found'
            else:
                distro = out.split(':')[1].strip()
                distro = ':%s' % distro
    else:
        distro = ''

    return {
        'hackedit': __version__,
        'python': platform.python_version(),  # "2.7.3"
        'bitness': 64 if sys.maxsize > 2**32 else 32,
        'qt': QT_VERSION_STR,
        'qt_api': 'PyQt5',
        'qt_api_ver': PYQT_VERSION_STR,
        'system': platform.platform() + distro,
        'pyqode.core': corev
    }
