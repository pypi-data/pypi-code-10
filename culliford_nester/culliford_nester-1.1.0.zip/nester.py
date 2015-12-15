"""This module "nester.py" contains a function print_lol which prints the contents of lists that may or may not include nestled lists."""

def print_lol(the_list, level):
	"""This function takes one positional argument called "the_list", which is any Python list (of - possibly - nested lists). Each data item 
	in the provided list is (recursively) printed to the screen on its own line."""

	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item, level+1)
		else:
			print(each_item)
