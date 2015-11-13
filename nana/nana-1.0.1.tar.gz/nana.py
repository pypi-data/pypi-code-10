from os import scandir
from subprocess import run
from time import sleep
from sys import exit

from cliar import CLI, ignore


class Nana(CLI):
    '''Nana keeps an eye on a directory and reacts when anything changes.'''

    def __init__(self):
        super().__init__()

        self.frame = 0
        self.doggie = [
            '\r^.   .  ^',
            '\r^ .   . ^',
            '\r^  .   .^',
            '\r^ .   . ^',
        ]

        self.mtimes = []

    @ignore
    def animate(self):
        '''Animate Nana's face'''

        print(self.doggie[self.frame], end='')
        self.frame += 1
        self.frame %= len(self.doggie)

    def _root(self, action, directory='.'):
        '''Run the action when anything in the given directory changes.

        :param action: action to run
        :param directory: directory to monitor
        '''

        mtimes = [item.stat().st_mtime for item in scandir(directory)]

        try:
            while True:
                self.animate()

                sleep(.5)

                new_mtimes = [item.stat().st_mtime for item in scandir(directory)]

                if new_mtimes != mtimes:
                    run(action.split())

                mtimes = new_mtimes

        except KeyboardInterrupt as e:
            exit('\r--- Ruff-Ruff! ---')


def main():
    Nana().parse()

if __name__ == '__main__':
    main()