""" This is my first module: nester.py for python,
	and it provides one function called print_lol.
	The following code is learned from book: <Head First Python>. """
def print_lol(the_list, indent=False, level=0):

	""" The function checks wether the 'the_list' has a nest list or not.
		if it has a nest list, then call itself again(recursive). if not,
		print the whole list.
		A sceond argument called "level" is used to insert tab-stops when
		 a nested list is ecountered."""

# comments

	for ei in the_list:
		if isinstance(ei, list):
			print_lol(ei, indent, level+1)
		else:
			if indent==True:
				for tab_stops in range(level):
					print('\t', end='')
			print(ei)
