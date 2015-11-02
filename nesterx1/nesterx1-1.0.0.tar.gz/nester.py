
def print_lol(_list):
    for item in _list:
        if isinstance(item, list):
            print_lol(item)
        else:
            print(item)
