# data store for information needed in building

import shelve

def open(filename):
    return shelve.open('build_info')
