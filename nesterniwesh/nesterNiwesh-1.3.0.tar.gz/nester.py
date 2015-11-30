"""This is the "nester.py module and it provides one function called print_lol
    which prints lists that may or may not include nested lists."""

def print_lol(the_list, indent = False, level = 0):
    """This function takes one positional argument called "the_list", which
        is any python list (of - possibly - nested lists). Each data item in the
        provided list is (recursively) printed to the screen on it's own line.
        A second argument called "indent" is used to specify(by you) if you want
        to use indention in your list or you don't want, by default it is turned
        off(i.e., its value is set to 'Fasle'). Also, a third argument called
        "level" is used to insert tab-stops when a nested list is encountered (its
        default value is set to '0'). """

    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1)

        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end = '')
            print(each_item)
