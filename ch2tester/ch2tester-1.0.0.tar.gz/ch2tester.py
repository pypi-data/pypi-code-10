""" this is the ch2tester.py module containing one function called
print_lol() which prints lists that may or may not include nested
lists"""
def print_lol(the_list):
    """ This function takes an list as an argument.  This list may
contain items which are lists themselves.  Each data item in the passed
list is recursively printed to screen on its own line"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)
