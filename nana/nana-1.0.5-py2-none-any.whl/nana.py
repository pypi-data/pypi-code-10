from __future__ import print_function

from os.path import getmtime
from subprocess import Popen
from time import sleep
from sys import exit

from cliar import CLI, ignore


class Nana(CLI):
    '''Nana keeps an eye on a directory and reacts when anything changes.'''

    frame = 0
    doggie = [
        '\r^.   .  ^',
        '\r^ .   . ^',
        '\r^  .   .^',
        '\r^ .   . ^',
    ]

    def _animate(self):
        '''Animate Nana's face'''

        print(self.doggie[self.frame], end='')

        self.frame += 1
        
        self.frame %= len(self.doggie)

    def _root(self, action, directory='.', timeout=1):
        '''Run the action when anything in the given directory changes.

        :param action: action to run
        :param directory: directory to monitor
        :param timeout: time beetween checks in seconds
        '''

        mtime = getmtime(directory)

        try:
            while True:
                self._animate()

                sleep(timeout)

                new_mtime = getmtime(directory)

                if new_mtime != mtime:
                    process = Popen(action.split(), shell=True)
                    stdout, stderr = process.communicate()

                mtime = new_mtime

        except KeyboardInterrupt as e:
            print('\r--- Ruff-Ruff! ---')
            exit()


def main():
    Nana().parse()


if __name__ == '__main__':
    main()