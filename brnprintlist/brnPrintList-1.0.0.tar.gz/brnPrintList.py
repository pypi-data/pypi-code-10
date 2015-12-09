#!/usr/bin/env	python3

'''
This is the 'brnPrintList.py' module and it provides one function called print_list()
which prints lists that may or may not include nested lists.
'''

def print_list(the_list):
	'''
	This function takes one positional argument called 'the_list', which is
	any Python list (of - possibility - nested lists). Each data item in the
	provided list is (recursively) printed to the screen on it's own line.
	'''
	for x in the_list:
		if isinstance(x, list):
			print_list(x)
		else:
			print(x) 
