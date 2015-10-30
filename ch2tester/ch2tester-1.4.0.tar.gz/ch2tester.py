""" this is the ch2tester.py module containing one function called
print_lol() which prints lists that may or may not include nested
lists"""
def print_lol(the_list,indent=False,level=0, fh=sys.stdout):
    """ This function takes an list as an argument.  This list may
contain items which are lists themselves.  Each data item in the passed
list is recursively printed to screen on its own line.  Level is 2nd arg
which will insert tab stops when nested list is encountered and arg indent
determines whether or not we will use tabs at all, fh determines where we
direct our output(file or screen)"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item,indent,level+1,fh)
        else:
            if(indent):
                for tab_stop in range(level):
                    print("\t", end='',file=fh)
            print(each_item, file=fh)
