"""
Simple nicer command line interface to easily rewrite the previous line of text.
"""


__version__ = '0.0.2'

import builtins




class OP:

    def __init__(self, overprinter, norpalprinter):
        self.reprint = overprinter
        self.print = norpalprinter

    def __call__(self, *args):
        return self.reprint(*args)

    def __getitem__(self, index):
        if index == 0:
            return self.reprint
        else:
            return self.print

    def __iter__(self):
        return iter((self.reprint, self.print))

def compensate(message, last):
    if(last):
        elen = len(last)-len(message)
    else:
        elen = 0
    if elen > 0:
        erase = ' '*elen
    else:
        erase = ''
    return message+erase

class overprint():

    def __init__(self, print_function=None, patch_builtin=False):
        self.last = None
        self._target_print = print_function
        self._origin_print = None
        self._monkey = patch_builtin
        self._in = False

    def _ok(self):
        if not self._in:
            raise ValueError("usage outside of context manager")
    
    def reprint(self, message):
        self._ok()
        p = compensate(message, self.last)
        self.last = message
        self._origin_print(p, end='\r')

    def nprint(self, message):
        self._ok()
        self._origin_print(compensate(message, self.last))
        if self.last is not None:
            self.reprint(self.last)

    def __enter__(self):
        self._in = True
        if self._target_print:
            self._origin_print = self._target_print
        else:
            self._origin_print = builtins.print
        if self._monkey:
            builtins.print = self.nprint

        return OP(self.reprint, self.nprint)

    def __exit__(self, *args):
        self._in = False
        if self._monkey:
            builtins.print = self._origin_print
        print('')

