"""
This is my module for practicing Python
"""

def print_lol(the_list, level=0):
	"""
	This function takes a list, and prints it out. 
	If there is a nested list, it is printed out indented.
	"""
	for each_item in the_list: #first loop
		if isinstance(each_item, list):
			print_lol(each_item, level+1)
		else:
			for ind in range(level):
				print('\t', end='')
			print(each_item)