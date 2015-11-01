# nester.py, tutorial for processing lists
def print_lol(the_list):
	#Given a list recurse and return
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item)
		else:
			print(each_item)



			
