#! /usr/bin/env/ python

""" Module contains one function (described below), and is part of training
	from the Head First: Python book. """

def print_lol(the_list, ident=False, tabsnum=0):

	""" print_lol function takes one list argument, iterates over its items
	and checks if any of those is a list. If no ident optional argument
	is not changed, the program will just print all items. If it's set
	to "True" then it will, then it will print items
	idented by a number of nested lists already found using
	tabsnum argument (optional, starting at 0)  and move on to the next one.
	  """

	for item in the_list:
		if isinstance(item, list):
			print_lol(item, ident, tabsnum+1)
		else:
			if ident:
				for i in range(tabsnum):
					print("\t", end='')
			print(item)
