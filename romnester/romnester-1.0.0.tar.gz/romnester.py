"""
This is my module for practicing Python
"""
def print_lol(the_list):
	for each_item in the_list: #first loop
		if isinstance(each_item, list):
			print_lol(each_item)
		else:
			print(each_item)