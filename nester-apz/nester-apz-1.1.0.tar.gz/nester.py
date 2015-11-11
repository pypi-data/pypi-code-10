#! /usr/bin/env/ python

""" Module contains one function (described below), and is part of training
	from the Head First: Python book. """

def print_lol(the_list, tabsnum):

	""" print_lol function takes one list argument, iterates over its items
	and checks if any of those is a list, if yes then it will invoke itself
	with this item as an argument, if not, then it will print the item
	idented by a number of nested lists already found using
	tabsnum argument (starting at 0)  and move
	on to the next one """

	for item in the_list:
		if isinstance(item, list):
			print_lol(item, tabsnum+1)
		else:
			for i in range(tabsnum):
				print("\t", end='')
			print(item)

