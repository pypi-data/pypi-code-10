""" This is my first module: nester.py for python,
	and it provides one function called print_lol.
	The following code is learned from book: <Head First Python>. """
def print_lol(the_list):

	""" The function checks wether the 'the_list' has a nest list or not.
		if it has a nest list, then call itself again(recursive). if not,
		print the whole list. """

# comments

	for ei in the_list:
		if isinstance(ei, list):
			print_lol(ei)
		else:
			print(ei)