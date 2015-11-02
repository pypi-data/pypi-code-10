
def print_lol(_list, level=0):
    for item in _list:
        if isinstance(item, list):
            print_lol(item, level+1)
        else:
            for tab_stop in range(level):
                print("\t", end = '')
            print(item)
