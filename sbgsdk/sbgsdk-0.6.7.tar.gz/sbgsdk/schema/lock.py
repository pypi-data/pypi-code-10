__author__ = 'Sinisa'

import os

def lock(name):
    try:
        os.mkdir(name + '.lock')
    except OSError:
        lock(name)
    return name + '.lock'


def unlock(name):
    os.rmdir(name + '.lock')