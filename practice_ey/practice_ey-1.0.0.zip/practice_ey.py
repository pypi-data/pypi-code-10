def print_lols(the_list):
	for each_items in the_list:
		if isinstance(each_items, list):
			print_lols(each_items)
		else:
			print('single'+ str(each_items))
