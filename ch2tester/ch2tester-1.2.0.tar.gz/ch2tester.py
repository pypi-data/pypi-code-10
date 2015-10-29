""" this is the ch2tester.py module containing one function called
print_lol() which prints lists that may or may not include nested
lists"""
def print_lol(the_list,level=0):
    """ This function takes an list as an argument.  This list may
contain items which are lists themselves.  Each data item in the passed
list is recursively printed to screen on its own line.  Level is 2nd arg
which will insert tab stops when nested list is encountered"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item,level+1)
        else:
            for tab_stop in range(level):
                print("\t", end='')
            print(each_item)
