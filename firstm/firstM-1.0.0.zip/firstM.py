"""This is a modul on the book of Headfirst Python.
Im studying the book and will share this module for study."""
def print_lol(the_list):
	"""This function is for listing data which type is list."""
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item)
		else:
			print(each_item)

			




        
