import sys

def print_lol(_list, indent = False, level=0, fn = sys.stdout ):
    for item in _list:
        if isinstance(item, list):
            print_lol(item, level+1, fn)
        else:
            for tab_stop in range(level):
                print("\t", end = '', file = fn)
            print(item, file = fn)
