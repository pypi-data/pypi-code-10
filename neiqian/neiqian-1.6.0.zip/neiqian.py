"""This is the "neiqian.py" module and it provides one function called print_lol()
	which prints lists that may or may not include nested lists."""
	
import sys
def print_lol(the_list, indent = False, level = 0, style = sys.stdout):
	""" Prints a list of (possibly) nested lists.

            This function takes a positional argument called "the_list", which
	    is any Python list (of - possible - nested lists). Each data item in the
	    provided list is (recursively) printed to the screen on it's own line.
	    A second argument called "indent" controls whether or not indentation is
	    shown on the display. This defaults to False: set it to True to switch on.
	    tab-stops when a nested list is encountered.
	    In the 1.5.0 version, a fourth argument is added to identify a place to write
	    your data to."""
		
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item, indent, level+1, style)
		else:
                        if indent:
                                for tab_stop in range(level):
                                        print("\t", end='', file=style)
                        print(each_item, file=style)
