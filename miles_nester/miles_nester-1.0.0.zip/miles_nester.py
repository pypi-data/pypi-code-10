"""This is the "nexter.py" module and it provides one function called print_lol()
	whice prints lists that may or may no include nested lists."""
def print_lol(the_list):
	"""This is function thakes one positional argument called "the_list", which
	is any Python list (of - possible - nested lists). Each data item in the"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item);
        else:
            print(each_item);
