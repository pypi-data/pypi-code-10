""" this is the nester.py module which contain a function print_lol used to print lists
which may or may not contain another list nested inside. """
def print_lol(the_list):
    """ This function accepts an argument 'the_list' , which is any python list or a nested list.
  Then each data item in that list is printed on screen."""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)
