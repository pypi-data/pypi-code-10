import os

class ChDir(object):
    '''
    This class is used to perform a change in directory
    for a specified block of code.

    Oftentimes code that changes directories explicitly
    sets and unsets the directory, thus causing the
    program to be in the wrong directory if an exception
    is thrown (usually crashes a program soon thereafter).

    This class is designed to be used by the 'with' keyword
    or blocked in a 'finally' block with an undo_ch operator.
    This way you get guarantees about returning to a home
    directory after code execution.

    Args:
        new_dir: The new directory into which the environment should move
        old_dir: The directory into which the enviroment should return upon exit
            (default current dir)
    '''
    def __init__(self, new_dir, old_dir=None):
        self.new_dir = new_dir
        if old_dir:
            self.saved_dir = old_dir
        else:
            self.saved_dir = os.getcwd()

    def ch_dir(self, new_dir=None, old_dir=None):
        if new_dir:
            self.new_dir = new_dir
        if old_dir:
            self.saved_dir = old_dir
        os.chdir(self.new_dir)

    def undo_ch(self):
        os.chdir(self.saved_dir)

    def __enter__(self):
        self.ch_dir()
        return self

    def __exit__(self, key, value, traceback):
        self.undo_ch()
