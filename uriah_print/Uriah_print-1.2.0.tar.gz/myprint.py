import sys
def print_list(myList, level = 0, f = sys.stdout):
    for element in myList:
        if isinstance(element, list):
            print_list(element, level + 1, f)
        else:
            for i in range(level):
                print('\t', end = '', file = f)
            print(element, file = f)