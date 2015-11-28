# allpaths.py - execute commands on multiple paths
#
# This software may be used and distributed according to the terms of
# the GNU General Public License version 2 or any later version.

'''execute commands on multiple paths'''

import mercurial.util
import mercurial.commands
import mercurial.cmdutil
from mercurial.i18n import _

#pylint:disable=invalid-name,broad-except,line-too-long


def _iter_over_paths(command, ui, repo, **opts):
    """execute given command on multiple paths"""
    # Extract our options and filter them out
    group = opts.pop('group', None) or 'paths'
    ignore_errors = opts.pop('ignore_errors', None)

    # Get the paths to push to.
    paths = ui.configitems(group)
    if not paths:
        raise mercurial.util.Abort(_('No paths defined in section %s') % group)

    # Used to avoid handling duplicate paths twice
    handled = {}

    # Act!
    for alias, path in paths:
        if path in handled:
            ui.note(_("Skipping %s as it aliases already handled %s\n") % (alias, handled[path]))
        else:
            handled[path] = alias
            try:
                command(ui, repo, path, **opts)
            except Exception as e:
                if not ignore_errors:
                    raise
                ui.warn(_('error handling %s: %s\n') % (alias, e))


def pushall(ui, repo, **opts):
    """execute pull on multiple paths"""
    _iter_over_paths(mercurial.commands.push, ui, repo, **opts)


def pullall(ui, repo, **opts):
    """execute push on multiple paths"""
    _iter_over_paths(mercurial.commands.pull, ui, repo, **opts)


def incomingall(ui, repo, **opts):
    """execute incoming on multiple paths"""
    _iter_over_paths(mercurial.commands.incoming, ui, repo, **opts)


def outgoingall(ui, repo, **opts):
    """execute outgoing on multiple paths"""
    _iter_over_paths(mercurial.commands.outgoing, ui, repo, **opts)


def _original_options(cmdname):
    """Gets list of given command options as specified in Mercurial core"""
    _, spec = mercurial.cmdutil.findcmd(cmdname, mercurial.commands.table)
    return spec[1]


EXT_OPTS = [
    ('g', 'group', 'paths', _('use a named group of paths')),
    ('', 'ignore-errors', None, _('continue execution despite errors')),
]

cmdtable = {
    "pushall": (
        pushall,
        EXT_OPTS + _original_options('push'),
        _('[-g GROUP] [--ignore-errors] <push options>')),
    "pullall": (
        pullall,
        EXT_OPTS + _original_options('pull'),
        _('[-g GROUP] [--ignore-errors] <pull options>')),
    "incomingall": (
        incomingall,
        EXT_OPTS + _original_options('incoming'),
        _('[-g GROUP] [--ignore-errors] <incoming options>')),
    "outgoingall": (
        outgoingall,
        EXT_OPTS + _original_options('outgoing'),
        _('[-g GROUP] [--ignore-errors] <outgoing options>')),
}
