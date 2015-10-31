import sys
def print_list(mylist, level = 0, FILE = sys.stdout):
    for person in mylist:
        if isinstance(person, list):
            print_list(person, level + 1, FILE)
        else:
            for i in range(level):
                print('\t', end = '', file = FILE)
            print(person, file = FILE)