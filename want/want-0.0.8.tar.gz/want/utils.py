import time
import os
import queue
from functools import wraps
from threading import Thread


def spend_time(func):
    """Calculate spend how many time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        url = args[0]
        print('\n%sStarting download photo from %s%s' %
              (colors.UNDERLINE, url, colors.ENDC))
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print('%s downloads done. Spend %.3f seconds.\n\n' % (url, end - start))
    return wrapper


def get_size(start_path='.'):
    """Get all file size in directory."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


class Mission:

    """Mission queue to execute."""

    def __init__(self, *, func, max_thread=5, results=None):
        self.queue = queue.Queue()
        self.func = func
        self.max_thread = max_thread
        if results is None:
            self.results = []
        else:
            self.results = results

    def __enter__(self):
        for x in range(self.max_thread):
            thread = Thread(target=self._threader)
            thread.daemon = True
            thread.start()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.queue.join()

    def send(self, *args):
        self.queue.put(args)

    def sendall(self, all):
        for args in all:
            self.queue.put(args)

    def _threader(self):
        while True:
            try:
                args = self.queue.get()
                self.results.append(self.func(*args))
                self.queue.task_done()
            except queue.Empty:
                pass


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def copyfileobj(fsrc, fdst, length=16 * 1024):
    """copy data from file-like object fsrc to file-like object fdst"""
    while 1:
        buf = fsrc.read(length)
        if not buf:
            break
        fdst.write(buf)
