""" This takes a list an iterates through it and prints each item.
	If an instance is found then it calls it's self and iterates through the list
	etc. """

def print_lol(the_list):
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item)
		else:
			print(each_item)
