"""This is the nester.py module and it provides one function called print_lol()
    which prints lists that may or may not include nested lists."""

def print_lol(the_list, indent=False, level=0, save_file = sys.stdout):
    """This function takes one positional argument called "the_list", which
    is any Python list (of - possibly - nested lists).  Each data item in the
    provided list is (recursively) printed to the screen on it's own line.  If
    items are in a nested list, they will be indented"""
    
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1, save_file)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end="", file = save_file)
            print(each_item, file = save_file)

            
