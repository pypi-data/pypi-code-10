#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
#  Copyright (C) 2015 Daniel Rodriguez
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import array
import argparse
import inspect
import io
import sys


# Small Py2/3 compatibility layer
if sys.version_info.major == 2:
    MAXSIZE = sys.maxint
    string_types = str, unicode
else:
    MAXSIZE = sys.maxsize
    string_types = str,


# GetChar from console
if sys.platform == 'win32':
    import msvcrt

    def getch(self, fin):
        return msvcrt.getch()
else:
    import tty
    import termios

    def getch(self, fin):
        fd = fin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fin.fileno())
            ch = fin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        return ch


# BrainF*ck Numeric Taype
class BfNum(object):
    '''Brainf*ck examples seem to rely on a byte type which rolls over

    255 + 1 -> 0
    0 - 1 -> 255

    This class simulates such numeric type with an adjustable bit size
    to cope with greater/smaller numeric types
    '''
    bitsize = 8

    @classmethod
    def _subclass(cls, name=None, bitsize=None):
        bitsize = bitsize or cls.bitsize
        name = name or (cls.__name__ + '_' + str(bitsize))
        return type(str(name), (cls,), dict(bitsize=bitsize))

    def __init__(self, bitsize=None):
        self.size = pow(2, bitsize or self.bitsize)
        self.value = 0

    def __int__(self):
        return self.value

    __long__ = __int__

    def __iadd__(self, other):
        self.value = (self.value + 1) % self.size
        return self

    def __isub__(self, other):
        self.value = (self.value - 1 + self.size) % self.size
        return self

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return self.value != other

    def __bool__(self, other):
        return self.value != 0

    __nonzero__ = __bool__


# BrainF*ck Command Decorator
def BfCommand(cmd):
    '''
    Decorates the function with ``_cmd`` attribute taken from the arg
    '''
    def decorator(function):
        function._cmd = cmd
        return function
    return decorator


# BrainF*ck Virtual Machine
class BrainFck(object):
    '''
    BrainF*ck interpreter/virtual machine

    The machine is configurable with following kwargs:
      - cellsize (default: 8)
        Size in bits of the numeric type to emulate. This types rollover when
        crossing the 0 and pow(2, cellsize) boundaries

      - totalcells (default: 30000)
        Size in cells in the virtual machine. Literature shows the default
        value to be expected by many test scripts

        Set it to ``0`` for unbounded size

      - extleft (defaults: True):
        Allow extension to the left. This applies only whilst the array has not
        reached its full size (if set)

      - prealloc (default: False)
        If the number of cells is limited, whether to preallocate them

      - wrapover (default: False)
        Wrap over cells boundaries if totalcells is set and all cells have been
        allocated (by preallocating or because the ``totalcells`` limit has
        been reached)

      - debug (default: False)
        Print the status and command to be evaluated

      - linemode (default: False)
        Read the input in lines and interpret each line as a program skipping
        blank lines

      - multiline (default: False)
        In ``linemode`` join lines until a blank line is seen

      - comments (default: False)
        In ``linemode`` skip lines starting with ``commentchar``

      - commentchar (default: #)
        Comment charachter for ``comments`` in ``linemode``

      - breakline (default: False)
        Print a breakline in between the output of the execution of multiple
        programs

    Input/Output:
      Controlled also through configuration variables

      - fin (default: sys.stdin)
        Stream from which input will be read

      - fout (default: sys.stdout)
        Stream to which input will be printed

      - fdebug (default: fout)
        Stream to print debug messages to

      - flushout (default: False)
        Flush out each write (including debug)

    Cells/Memory:
      - cells: access to the array of memory cells

        The machine checks boundaries and will not go below 0 or above the
        maximum total number of cells configured

      - bfnum: class holding the numeric type with the configure bitsize for
        this machine.

    Command Processing:
      - cmd_procs (dict): holds a reference per command to a method to process
        the command. Automatically filled with methods which have been
        decorated with BfCommand

    Command index:
      - idx (start: -1)
        Current command index. Increased when a command is read

    Constants:
      - maxptr
        Holds the right limit in cells of the virtual machine

      - csize
        Length of the numeric value (power of 2 of cellsize)

    Status:
      - cmd (start: '')
        Current command being processed

      - ptr (start: 0)
        Current cell for get/set/check operations

      - loopskip (start: 0)
        if > 0, it will skip commands until the matching amount of ']' has been
        seen. While positive, seeing a '[' will increase its value by 1

      - loops (start: [])
        Stores index in input of '[' commands until they must be skipped

      - loopback (start: -1)
        If >= 0, the value indicates a jump to such command index

    Commands:

      Methods decorated with ``BfCommand(cmd)`` will be added to a dictionary
      ``cmd_procs`` using ``cmd`` as the key.

      Method retrieval when a command is read (unless commands are being
      skipped inside a loop) will be done using the dictionary

      The commands manipulate the ``Status`` variables

      Decoration allows for easy addition of new commands

      Internally ``None`` is used as a virtual NOP command when the commands
      inside a loop have to be skipped

      Commands are deliberately kept as simple as possible in that they don't
      do any memory management or command index manipulation. If such an action
      may be needed it will tackled by the main loop using the information in
      the status variables modified by the commands
    '''
    totalcells = 30000  # 0 for unlimited
    prealloc = False  # pre-alloc or on the spot
    cellsize = 8  # in bits
    extleft = True  # extend to the left when dynamically allocating
    wrapover = True  # wrapover cell boundaries if totalcells is set and alloc
    nonumclass = False  # use internal numerics
    fin = None  # file object for input
    fout = None  # file object for output
    fdebug = None  # file object for debug output
    flushout = False  # flushout each write (including debug)

    linemode = False  # each line of files is a script
    multiline = False  # join lines in linemode
    comments = False  # in linemode skip lines starting with commentchar
    commentchar = '#'  # character for comments in linemode
    breakline = False  # breakline in between output of multiple programs

    debug = False  # print current status and command to be evaluated

    def __init__(self, **kwargs):
        '''
        Initializes the machine (not to confuse with resetting the status)

          - It prepares the dictionary of commands

          - It configures the "configuration" variables

          - It sets the constants for maximum pointer length and cell
            allocation

          - Configures the numeric class

          - Prepares the input/output streams
        '''
        # Command reference
        self.cmd_procs = dict()

        # Look for decorated commands
        members = inspect.getmembers(self, inspect.ismethod)
        for name, method in members:
            try:
                self.cmd_procs[method._cmd] = method
            except AttributeError:
                pass  # The method has not been decorated

        # Parse kwargs and match them to the existing configuration variables
        for name, value in kwargs.items():
            if hasattr(self, name):
                setattr(self, name, value)

        # Constant holding the right boundary of the cells
        self.maxptr = self.totalcells - 1 if self.totalcells else MAXSIZE

        # Numeric type for each cell
        self.csize = pow(2, self.cellsize)
        if self.nonumclass:
            self.bfnum = int
        else:
            self.bfnum = BfNum._subclass(bitsize=self.cellsize)

        # input / output
        self.fin = self.fin or sys.stdin
        self.fout = self.fout or sys.stdout
        self.fdebug = self.fdebug or self.fout

    def reset(self):
        '''Resets the virtual machine to the default status'''

        self.mmu_init()  # initialize memory

        # Reset status variables
        self.cmd = ''
        self.idx = -1
        self.ptr = 0
        self.loopskip = 0
        self.loops = []
        self.loopback = -1

    def writeout(self, *args):
        print(*args, end='', file=self.fout)
        if self.flushout:
            self.fout.flush()

    def debug_out(self, *args):
        print(*args, file=self.fdeb)
        if self.flushout:
            self.fdeb.flush()

    def debug_config(self):
        '''Prints config debug information'''
        if self.debug:  # print soem debug info if requested
            self.debug_out('fin', self.fin)
            self.debug_out('fout', self.fout)
            self.debug_out('fdebug', self.fdebug)
            self.debug_out('nonumclass', self.nonumclass)
            self.debug_out('bfnum', self.bfnum)
            self.debug_out('cellsize', self.cellsize)
            self.debug_out('csize', self.csize)
            self.debug_out('maxptr', self.maxptr)
            self.debug_out('totalcells', self.totalcells)

    def debug_status(self):
        '''Prints status debug information'''
        if self.debug:  # print soem debug info if requested
            self.debug_out('idx:', self.idx)
            self.debug_out('ptr:', self.ptr)
            self.debug_out('cell[ptr]:', int(self.cells[self.ptr]))
            self.debug_out('cellcount:', len(self.cells))
            self.debug_out('loopskip:', self.loopskip)
            self.debug_out('loops:', self.loops)
            self.debug_out('loopback:', self.loopback)

            self.debug_out('-' * 50)
            self.debug_out('cmd:', cmd)

    def runfiles(self, *args):
        '''
        It opens ``filenames`` (args) in read/binary mode to get an unprocessed
        stream of bytes and executes the program(s)

        Args:
          args: paths to files
        '''
        for arg in args:
            f = io.open(arg, 'rb')  # open in r + b mode
            self.run(f)
            f.close()

    def run(self, f):
        '''
        Runs a BrainF*ck program

        Args:
          f: file (like) object or string
             If a string is passed it will be internally converted to a file
             like object

        In non ``linemode`` the contents of the file will be executed as a
        single script

        If in ``linemode`` the file will be read line by line (skipping empty
        lines)

        If in ``multiline`` non-empty lines will be joined until a blank line
        is seen

        If, additionally, in ``comments`` mode, then lines starting with the
        ``commentschar`` character will also be skipped
        '''
        # Check if a string was passed and turn it into a file-like object
        if isinstance(f, string_types):
            f = io.StringIO(f)

        if not self.linemode:
            self.execute(f)
        else:
            lines = []  # buffer to keep seen lines
            for line in f:
                # Check comments mode and if needed skip them
                if self.comments:
                    if line.startswith(self.commentchar):
                        continue

                strippedline = line.rstrip('\r\n')
                if strippedline == '':
                    # blank line seen, execute if something has been seen
                    if lines:
                        self.execute(io.StringIO(''.join(lines)))
                        lines = []
                else:
                    # no comment and no blank line ... save the line
                    lines.append(line)
                    if not self.multiline:
                        # single line mode, execute the appended line
                        self.execute(io.StringIO(''.join(lines)))
                        lines = []

            # Execute remaining lines
            if lines:
                self.execute(io.StringIO(''.join(lines)))

    def mmu_init(self):
        # Allocate (or not) the memory for the cells
        numcells = self.totalcells * self.prealloc
        self.cells = [self.bfnum() for x in range(0, numcells)]

    def mmu(self):
        '''Manages memory expansion (if needed)

        1. Unbounded case (totalcells = 0)
           The machine expands the cells left and right as needed

        2. Bounded but not yet fully allocated
           The machine expands the cells left and right as needed

        3. Bounded and fully allocated and wrapover is True
           Wrap over the boundaries

        4. Else ... fix the ptr to remain within bounds
        '''
        lcells = len(self.cells)

        if not self.totalcells or lcells < self.totalcells:
            # 1. and 2. - Unbounded mode or bounded but not fully allocated
            if self.ptr >= lcells:  # expand right if reached memory limit
                for i in range(0, self.ptr - lcells + 1):
                    self.cells.append(self.bfnum())

            elif self.ptr < 0:  # expand left if below the 0 mark - fix ptr
                self.ptr = 0
                if self.extleft:  # can extend to the left
                    for i in range(0, abs(self.ptr)):
                        self.cells.insert(0, self.bfnum())

        elif self.wrapover:  # 3. wrap over in bounded mode and fully allocated
            if self.ptr >= lcells:
                self.ptr = 0
            elif self.ptr < 0:
                self.ptr = lcells - 1

        else:  # 4. no wrapping over allowed - reset the pointers
            self.ptr = min(self.ptr, lcells - 1)
            self.ptr = max(self.ptr, 0)

    def execute(self, f):
        '''
        Actual execution of the BrainF*ck program

        Args:
          f: file (like) object

        The machine is "reset" at the beginning and in each loop
          - Cell (append) memory management is done in dynamic mode (if needed)
            - To the right if going over the limit
            - To the left if going below the 0 mark
          - Jumps in program text are performed if needed
          - Next command is fetched
          - On "no command" (EOF) the loop is exited
          - If a command processor exists for the command it is fetched
            - In case a loop has to be skipped the command processor is fetched
              using the internal NOP command (None)
          - If any command processor has been fetched is invoked
          - If internal numerics are in used, do an overflow check on the cell
        '''
        self.reset()  # reset the machine on each run

        self.debug_config()  # print configuration debug info

        while True:
            # Memory management
            self.mmu()

            # Process jump backwards flag
            if self.loopback >= 0:
                # Go to loopback + 1, skipping the loop start cmd
                f.seek(self.loopback + 1)
                # idx starts at -1 and the +1 from above is canceled
                self.idx = self.loopback
                self.loopback = -1  # reset the flag

            # Command input processing
            self.cmd = cmd = f.read(1)  # read next command
            self.idx += 1  # keep track of read commands

            self.debug_status()

            if cmd == '':
                break  # EOF reached

            # Choose NOP (if skipping loop) or read command
            cmdkey = None if self.loopskip else cmd
            try:
                cmd_proc = self.cmd_procs[cmdkey]
            except KeyError:
                # This effectively separates other exceptions from the one
                # fetching the command processor from the dictionary
                continue  # no such command exists

            # Command processor found, execute
            cmd_proc()

            # Do boundary adjustment if operations are done internally
            if cmd in ['+', '-'] and self.nonumclass:
                self.cells[self.ptr] = (
                    (self.cells[self.ptr] + self.csize) % self.csize)

        if self.breakline:
            self.writeout('\n')

    @BfCommand(None)
    def proc_loopskip(self):
        '''Skips commands until the next closing loop command is found

        Loop commands '[' and ']' seen while looping will be skipped by
        adding them and substracting them from the loopskip count
        '''
        if self.cmd == '[':
            self.loopskip += 1
        elif self.cmd == ']':
            self.loopskip -= 1

    @BfCommand('+')
    def proc_increment(self):
        '''Increments by one the value of the current cell'''
        self.cells[self.ptr] += 1

    @BfCommand('-')
    def proc_decrement(self):
        '''Decrements by one the value of the current cell'''
        self.cells[self.ptr] -= 1

    @BfCommand('[')
    def proc_whilebegin(self):
        '''If the current cell is 0, increases the loopskip counter to skip the
        current loop.

        Otherwise it marks the position in the command index seen
        '''
        if self.cells[self.ptr] == 0:
            self.loopskip += 1
        else:
            self.loops.append(self.idx)

    @BfCommand(']')
    def proc_whileend(self):
        '''If the current cell is 0, it removes the entry for the loop start to
        simply carry on

        Otherwise it sets loopback to the command index to jump to
        '''
        if self.cells[self.ptr] == 0:
            self.loops.pop()
        else:
            self.loopback = self.loops[-1]

    @BfCommand('>')
    def proc_forward(self):
        '''Increments cell pointer by one'''
        self.ptr += 1

    @BfCommand('<')
    def proc_backwards(self):
        '''Decrements cell pointer by one'''
        self.ptr -= 1

    @BfCommand('.')
    def proc_output(self):
        '''Outputs in char format the value of the current cell'''
        self.writeout(chr(self.cells[self.ptr]))

    @BfCommand(',')
    def proc_input(self):
        '''Reads input in char format the value of the current cell'''
        self.cells[self.ptr] = ord(getch(self.fin))


def parse_args():
    '''Parses command line arguments and returns the "parser" instance'''
    parser = argparse.ArgumentParser(
        description='BrainF*ck Interpreter/Virtual Machine',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('script', action='append',
                        help=('BrainF*ck script to execute (can be specified'
                              ' multiple times'))

    parser.add_argument('--totalcells', '-tc', required=False,
                        default=30000, type=int,
                        help='Size of memory in cells (set to 0 for unbounded')

    parser.add_argument('--prealloc', '-pa', required=False,
                        action='store_true',
                        help='Preallocate cells if a memory size has been set')

    parser.add_argument('--noextleft', '-nl', required=False,
                        action='store_true',
                        help=('Do not extend the cells to the left in dynamic'
                              'allocation'))

    parser.add_argument('--wrapover', '-wo', required=False,
                        action='store_true',
                        help=('If the number of totalcells is limited, wrap'
                              ' over the boundaries when the amount of'
                              ' totalcells has already been allocated'))

    parser.add_argument('--cellsize', '-cs', required=False,
                        default=8, type=int,
                        help='Size in bits of each cell')

    parser.add_argument('--nonumclass', '-nn', required=False,
                        action='store_true',
                        help='Do numerics directly rather than with a class')

    parser.add_argument('--debug', '-db', required=False,
                        action='store_true',
                        help='Print debug information')

    parser.add_argument('--linemode', '-lm', required=False,
                        action='store_true',
                        help=('In line mode each line of a provided script'
                              ' file will be interpreted as a single script.'
                              ' Empty lines will be skipped'))

    parser.add_argument('--multiline', '-ml', required=False,
                        action='store_true',
                        help=('In linemode subsequent lines will be joined'
                              ' until a blank line is seen'))

    parser.add_argument('--comments', '-co', required=False,
                        action='store_true',
                        help=('In line mode lines starting with # will be'
                              ' skipped'))

    parser.add_argument('--commentchar', '-cc', required=False,
                        default='#',
                        help=('Char which indicates a line is a comment'))

    parser.add_argument('--breakline', '-br', required=False,
                        action='store_true',
                        help=('Print a break line in between output of'
                              ' scripts'))

    parser.add_argument('--flushout', '-fo', required=False,
                        action='store_true',
                        help=('Flush output on each write (meant for broken'
                              ' buffering like Python 2.x under Win32'))

    return parser.parse_args()


def pybrainfuck():
    '''Runs a BrainF*ck Machine with command line arguments'''

    args = parse_args()

    bfck = BrainFck(
        totalcells=args.totalcells,
        prealloc=args.prealloc,
        cellsize=args.cellsize,
        extleft=not args.noextleft,  # inverted (machine default is True)
        wrapover=args.wrapover,
        nonumclass=args.nonumclass,
        linemode=args.linemode,
        multiline=args.multiline,
        comments=args.comments,
        commentchar=args.commentchar,
        breakline=args.breakline,
        flushout=args.flushout,
        debug=args.debug)

    bfck.runfiles(*args.script)


if __name__ == '__main__':
    pybrainfuck()
