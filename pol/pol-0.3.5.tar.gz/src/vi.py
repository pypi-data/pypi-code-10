""" curses user interface for pol. """

import os

import pol.safe
import pol.session

import urwid
import urwidtrees
import urwidtrees.tree

class SessionTree(urwidtrees.tree.Tree):
    """ Interprets pol's Session object as a tree of widgets as follows

            root                ()
              Container @12     (0,)
                 Entry          (0, 0)
                 Entry          (0, 1)
              Container @33     (1, 0)
                 Entry          (1, 1)
                 """
    def __init__(self, session):
        self.session = session
        self.root = ()

    # Start interface of Tree.
    def __getitem__(self, pos):
        return urwid.SelectableIcon(str(pos))
    def parent_position(self, pos):
        if not root:
            return None
        return pos[1:]
    def first_child_position(self, pos):
        if len(pos) == 2:
            return None
        return pos + (0,)
    def last_child_position(self, pos):
        if not pos:
            return (len(self.session.containers) - 1,)
        if len(pos) == 1:
            return pos + (len(self.session.containers[pos[0]].entries) - 1,)
        return None
    def next_sibling_position(self, pos):
        if len(pos) == 1:
            if pos[0] >= len(self.session.containers):
                return None
            return (pos[0]+1,)
        if len(pos) == 2:
            if pos[0] >= len(self.session.containers[0].entries):
                return None
            return (pos[0], pos[1]+1)
        return None
    def prev_sibling_position(self, pos):
        ret = list(pos)
        ret[-1] -= 1
        if not ret[-1]:
            return None
        return tuple(ret)
    def depth(self, pos):
        return len(pos) - 1

class VisualPol(object):
    def __init__(self, program):
        self.program = program
    def unhandled_input(self, key):
        if key == 'q':
            raise urwid.ExitMainLoop()
    def main(self):
        with pol.safe.open(os.path.expanduser(self.program.safe_path),
                           nworkers=self.program.args.workers,
                           use_threads=self.program.args.threads) as safe:
            self.safe = safe
            self.session = pol.session.Session(safe)
            self.session.unlock('m') # TODO

            tree = urwidtrees.widgets.TreeBox(
                    urwidtrees.decoration.IndentedTree(
                        SessionTree(self.session)))

            self.loop = urwid.MainLoop(tree,
                        unhandled_input=self.unhandled_input)
            self.loop.run()

def main(program):
    VisualPol(program).main()
