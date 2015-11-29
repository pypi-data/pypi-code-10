# Released under GPL3 terms (see LICENSE)

"""Provide information about storage devices (needs psutil)"""

from . import (rate, cache, convert, io)
import os
from collections.abc import Mapping as _Mapping
try:
    import psutil as _psutil
except ImportError:
    io.croak('Please install python3-psutil')


# TODO: os.path.ismount(path) returns False if path is not readable:
# https://bugs.python.org/issue2466
def ismount(path):
    """Test whether a path is a mount point"""
    try:
        s1 = os.lstat(path)
    except OSError:
        # It doesn't exist -- so not a mount point. :-)
        return False
    else:
        # A symlink can never be a mount point
        import stat
        if stat.S_ISLNK(s1.st_mode):
            return False

    if isinstance(path, bytes):
        parent = os.path.join(path, b'..')
    else:
        parent = os.path.join(path, '..')
    parent = os.path.realpath(parent)  # This fixes the issue.
    try:
        s2 = os.lstat(parent)
    except OSError as e:
        return False

    dev1 = s1.st_dev
    dev2 = s2.st_dev
    if dev1 != dev2:
        return True     # path/.. on a different device as path
    ino1 = s1.st_ino
    ino2 = s2.st_ino
    if ino1 == ino2:
        return True     # path/.. is the same i-node as path
    return False


class Bytes(int):
    def __str__(self):
        return convert.num2str(self, binary=False) + 'B'

class Byterate(Bytes):
    def __str__(self):
        return super().__str__() + '/s'

class Percent(float):
    def __str__(self):
        return str(round(self)) + ' %'

class Path(str):
    def __new__(cls, path):
        return super().__new__(cls, os.path.realpath(os.path.normpath(os.path.expanduser(path))))

    def __init__(self, path):
        if path.startswith('/home/'):
            self.__tildified = '~' + path[6:]
        else:
            self.__tildified = path
        self.__full = path

    def __str__(self):
        return self.__tildified

    def __repr__(self):
        return self.__full

class UnquotedString(str):
    __repr__ = str.__str__


@cache.timeout(seconds=0.5)
def _cached_io_counters(*args, **kwargs):
    return _psutil.disk_io_counters(*args, **kwargs)


class Mountpoint(_Mapping):
    """
    Provide information about a mountpoint as a dictionary

    >>> mp = Mountpoint('/')
    >>> mp['path']
    '/'
    >>> mp['devpath']
    '/dev/sda1'

    Available attributes:
      Non-variables: path, devpath, devname, fs, mounted
      Usage: free, used, total, free%, used%
      IO rates: read, write, rw

    Those attributes are human-readable strings. Each attribute has a
    machine-readable counterpart with a leading '_'. For paths, the '_'
    variant resolves links, and numbers are integers.

    >>> mp['free%']
    '54 %'
    >>> mp['_free%']
    54.1
    >>> mp['read']
    '45 kB/s'
    >>> mp['_read']
    49385

    """

    def __init__(self, path, iosamples=3):
        """
        `path` is the path to the mountpoint.
        `iosamples` is the number of previous read/write/rw values that are
        used to compute an average.
        """
        self._fixed = { 'path': Path(path) }
        for partition in _psutil.disk_partitions():
            if partition.mountpoint == repr(self._fixed['path']):
                self._fixed['devpath'] = Path(os.path.realpath(partition.device))
                self._fixed['devname'] = UnquotedString(os.path.basename(self._fixed['devpath']))
                self._fixed['fs'] = UnquotedString(partition.fstype)

        if 'devname' not in self._fixed:
            raise RuntimeError('Could not find mountpoint: {!r}'.format(self._fixed['path']))

        self._usage = { 'free': Bytes(0), 'used': Bytes(0), 'total': Bytes(0),
                        'used%': Percent(0), 'free%': Percent(0) }
        self._io = { 'read': Byterate(0), 'write': Byterate(0), 'rw': Byterate(0) }
        self._io_read = rate.RatePerSecond()
        self._io_write = rate.RatePerSecond()
        self._io_rw = rate.RatePerSecond()
        self._io_read_avg = rate.Average(samples=iosamples)
        self._io_write_avg = rate.Average(samples=iosamples)
        self._io_rw_avg = rate.Average(samples=iosamples)

        self._keys = tuple(self._fixed) + tuple(self._usage) + tuple(self._io)
        self._keys += tuple('_'+k for k in self._keys) + ('mounted', '_mounted')

    @property
    @cache.timeout(seconds=0.5)
    def usage(self):
        """Return a dictionary with keys: free, free%, used, used%, total"""
        # io.debug('----- Getting usage')
        usage = _psutil.disk_usage(self['_path'])
        return { 'free': Bytes(usage.free),
                 'used': Bytes(usage.used),
                 'total': Bytes(usage.total),
                 'used%': Percent(usage.percent),
                 'free%': Percent(100-usage.percent) }

    @property
    @cache.timeout(seconds=0.5)
    def io(self):
        """Return a dictionary with IO rates: read, write, rw"""
        # io.debug('----- Getting disk io counters for {}'.format(self['devname']))
        devices = _cached_io_counters(perdisk=True)
        counters = devices[self['devname']]
        read_rate = self._io_read.update(counters.read_bytes)
        write_rate = self._io_write.update(counters.write_bytes)
        rw_rate = self._io_rw.update(counters.read_bytes + counters.write_bytes)
        return { 'read': Byterate(self._io_read_avg.update(read_rate)),
                 'write': Byterate(self._io_write_avg.update(write_rate)),
                 'rw': Byterate(self._io_rw_avg.update(rw_rate)) }

    @property
    def iosamples(self):
        return self._io_read_avg.samples
    @iosamples.setter
    def iosamples(self, samples):
        self._io_read_avg.samples = samples
        self._io_write_avg.samples = samples
        self._io_rw_avg.samples = samples

    @property
    @cache.timeout(seconds=0.5)
    def mounted(self):
        return ismount(self['_path'])

    def __getitem__(self, key):
        if key == 'mounted':
            return self.mounted
        elif key == '_mounted':
            return str(self.mounted)
        else:
            if key[0] == '_':
                func = repr
                key = key[1:]
            else:
                func = str

            if key in self._fixed:
                return func(self._fixed[key])
            elif key in self._usage:
                return func(self.usage[key]) if self.mounted else None
            elif key in self._io:
                return func(self.io[key]) if self.mounted else None
            else:
                raise KeyError(key)

    def __len__(self):
        return len(self._keys)

    def __iter__(self):
        return iter(self._keys)

    def __lt__(self, other):
        if type(other) != type(self):
            return NotImplemented
        return self['path'] < other['path']

    def __eq__(self, other):
        if type(other) != type(self):
            return NotImplemented
        return self['path'] == other['path']

    def __hash__(self):
        return hash(self._fixed['path'])

    def __repr__(self):
        r = '<{}'.format(type(self).__name__)
        for k in self._keys:
            r += ', {}={}'.format(k, repr(self[k]))
        r += '>'
        return r


class Mountpoints(_Mapping):
    """Auto-updated dictionary of mountpoints"""

    def __init__(self, blacklist=None, whitelist=None, iosamples=3):
        self._mountpoints = {}
        self._hooks = { 'mounted': [], 'unmounted': [], 'updated': [] }
        self._whitelist = []
        self._blacklist = []
        if blacklist is not None: self.blacklist = blacklist
        if whitelist is not None: self.whitelist = whitelist
        self.iosamples = iosamples

    @property
    def whitelist(self):
        """List of mountpoint paths to not ignore"""
        return self._whitelist
    @whitelist.setter
    def whitelist(self, lst):
        self._whitelist = tuple(set(os.path.normpath(path) for path in lst))
        self._is_wanted.clearcache()

    @property
    def blacklist(self):
        """List of mountpoint paths to ignore"""
        return self._blacklist
    @blacklist.setter
    def blacklist(self, lst):
        self._blacklist = tuple(set(os.path.normpath(path) for path in lst))
        self._is_wanted.clearcache()

    @property
    def iosamples(self):
        """Number of samples to compute average IO rates"""
        return self._iosamples
    @iosamples.setter
    def iosamples(self, samples):
        self._iosamples = samples
        for mp in self._mountpoints:
            mp.iosamples = samples

    @cache.timeout(seconds=-1)
    def _is_wanted(self, path):
        """Return whether `path` is part of `whitelist` or not part of `blacklist`"""
        # io.debug('----- Checking if {} is wanted'.format(path))
        def partof(lst, path):
            for lst_path in lst:
                if path == lst_path or \
                   lst_path[-1] == '*' and path.startswith(lst_path.rstrip('*').rstrip('/')):
                    return True
            return False

        if self.whitelist:
            # If whitelist is not empty, blacklist doesn't matter
            return partof(self.whitelist, path)
        else:
            return not partof(self.blacklist, path)

    def poll(self):
        """Add/Remove/Update mountpoints"""
        current_paths = tuple(part.mountpoint for part in _psutil.disk_partitions(all=False))
        mountpoints = self._mountpoints
        for path in current_paths:
            if self._is_wanted(path):
                try:
                    self._run_hooks('updated', mountpoints[path])
                except KeyError:
                    mountpoints[path] = Mountpoint(path, iosamples=self._iosamples)
                    self._run_hooks('mounted', mountpoints[path])
            elif path in mountpoints:
                del(mountpoints[path])

        for path in tuple(mountpoints):
            if path not in current_paths:
                self._run_hooks('unmounted', mountpoints[path])
                del(mountpoints[path])

    def add_hook(self, hook, callback):
        """
        Add `callback` to `hook`

        `hook` must be 'mounted', 'unmounted' or 'updated'.
        `callback` is passed a `Mountpoint` object.
        """
        if hook not in self._hooks:
            raise ValueError('Invalid hook: {!r}'.format(hook))
        self._hooks[hook].append(callback)

    def _run_hooks(self, name, *args, **kwargs):
        for callback in self._hooks[name]:
            callback(*args, **kwargs)

    def __getitem__(self, item):
        self.poll()
        return self._mountpoints[item]

    def items(self):
        self.poll()
        return super().items()

    def __len__(self):
        self.poll()
        return len(self._mountpoints)

    def __iter__(self):
        self.poll()
        return iter(self._mountpoints)

    def __repr__(self):
        # self.poll()
        return repr(self._mountpoints)

    def __hash__(self):
        return id(self)
