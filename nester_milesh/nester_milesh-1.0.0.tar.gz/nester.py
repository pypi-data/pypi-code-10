"""Prints out Nested Lists"""

def print_lol(the_list):
	for an_entry in the_list:
		if isinstance(an_entry, list):
			print_lol(an_entry)
		else:
			print(an_entry)


			
