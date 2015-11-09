'''This is "nester.py" module, it provides a function named print_li(), it is designed to print a list which may or may not contain a nested list.'''
def print_li(the_list, tab_nums):
    """This function requires a location parameter named "the_list", it can be any list or nested list. Each member of the list will output onto the screen, each member occupy a line.	"""
    for each in the_list:
        if isinstance(each, list):
            print_li(each)
        else:
			for tab_num in range(tab_nums):
				print('\t', end='')
            print(each)