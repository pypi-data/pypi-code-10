# Released under GPL3 terms (see LICENSE)

"""Provide information about new packages"""

from . import (inotify, io)
import os
import subprocess
import time
import locale as _locale
_locale.setlocale(_locale.LC_ALL, '')


# All package manager classes should inherit from _pkgmgr so NAMES at the end
# of this file can keep a list of all supported package managers.
class _pkgmgr():

    def wait_for_cache_update(self):
        """Block until the number of available packages has changed"""
        raise NotImplementedError

    def count_new_packages(self):
        """Return the number of packages available for installation"""
        raise NotImplementedError


class apt(_pkgmgr):
    _CACHE_FILE = '/var/cache/apt/pkgcache.bin'

    # TODO: Using python3-apt might be a better way to count new packages, and
    # 'dist-upgrade' probably doesn't work on stable.

    # Also, using inotify on the cache file isn't very precise (cache is
    # written multiple times and doesn't always exist), but I can't think of a
    # better way and it seems to work.

    _COUNT_CMD = ('nice -19 apt-get dist-upgrade --simulate | grep "^Inst " | wc --lines')

    def __init__(self):
        self._prev_cache_update = 0

    def wait_for_cache_update(self):
        """Block until the number of available packages has (or may have) changed"""

        # Cache file does not always exist, but it should appear eventually.
        tries = 0
        while not os.path.exists(self._CACHE_FILE):
            time.sleep(1)
            tries += 1
            if tries > 10:
                io.croak('Cache file doesn\'t exist: {!r}'.format(self._CACHE_FILE))

        inotify.wait(self._CACHE_FILE, events=('close_write',))

        # Ignore changing cache if it changed recently
        now = time.time()
        if now - self._prev_cache_update < 10:
            self.wait_for_cache_update()
        self._prev_cache_update = now

    def count_new_packages(self):
        """Return the number of packages available for installation"""
        fail_msg = 'Counting new packages failed: '
        try:
            num = subprocess.check_output(self._COUNT_CMD,
                                          shell=True,
                                          universal_newlines=True).strip()
        except Exception as e:
            io.croak(fail_msg + str(e))
        else:
            try:
                num = int(num)
            except ValueError:
                io.croak(fail_msg + '{!r} returned {!r}'.format(self._COUNT_CMD, num))
            else:
                return num


# List of classes that derived from _pkgmgr
NAMES = tuple(local.__name__ for local in locals().values()
              if type(local) is type and _pkgmgr in local.mro() \
              and local.__name__[0] != '_')
