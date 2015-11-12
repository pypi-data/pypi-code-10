import sys

class StdRedirector(object):
    '''
    This class is used to perform a change in stdout and stderr
    for a specified block of code.

    This class is designed to be used by the 'with' keyword.
    This way you get guarantees about returning to the original
    sys.stdout and sys.stderr.

    Args:
        stdout: The new stdout file-like object (default no change)
        stderr: The new stderr file-like object (default no change)
    '''
    def __init__(self, stdout=None, stderr=None):
        self.stdout = stdout
        self.stderr = stderr
        self.stored_stdout = None
        self.stored_stderr = None

    def __enter__(self):
        if self.stdout:
            self.stored_stdout = sys.stdout
            sys.stdout = self.stdout
        if self.stderr:
            self.stored_stderr = sys.stderr
            sys.stderr = self.stderr

    def __exit__(self, exc_type, exc_value, traceback):
        # Ensure we flush requests before swapping back
        self.flush()
        if self.stdout:
            sys.stdout = self.stored_stdout
        if self.stderr:
            sys.stderr = self.stored_stderr

    def flush(self):
        try:
            if self.stdout:
                self.stored_stdout.flush()
            if self.stderr:
                self.stored_stderr.flush()
        except AttributeError:
            pass
