"""This module may save you a lot of time 
and you can judt concentrate on your own 
piece of work"""
def print_lol(list):
	"""To tell if an item in a list is also a list"""
	for each_item in list:
		if isinstance(each_item, list):
			print_lol(each_item)
		else:
			print(each_item)
		