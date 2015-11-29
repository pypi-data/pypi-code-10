# Released under GPL3 terms (see LICENSE)

"""Stats about mail accounts"""

# TODO: Add MailAccountIMAP class.

from . import (inotify, io)
import os.path


def get_account(identifier):
    identifier = str(identifier)
    if ':' not in identifier:
        io.croak('Missing protocol in mail account: {!r}'.format(identifier))

    proto, identifier = identifier.split(':', 1)
    if proto.lower() == 'maildir':
        return MailAccountMaildir(identifier)
    else:
        io.croak('Unknown mail protocol: {!r}' .format(proto))


class MailAccountMaildir():
    def __init__(self, path):
        self._path = os.path.expanduser(path)
        self._path_new = os.path.normpath(self._path+'/new')
        self._path_cur = os.path.normpath(self._path+'/cur')

    def wait(self):
        """Block until the number of seen/unseen mails changes"""
        inotify.wait(self._path_new, self._path_cur,
                     events=('moved_from', 'moved_to', 'create', 'delete'))
        io.debug('Mail count in {!r} has changed'.format(self._path))

    def unseen_count(self):
        """Return the number of unseen mails"""
        return self._count_mail(self._path_new)

    def seen_count(self):
        """Return the number of seen mails"""
        return self._count_mail(self._path_cur)

    def _count_mail(self, path):
        try:
            return len(os.listdir(path))
        except:
            io.croak('Not a maildir directory: {!r}'.format(path))
