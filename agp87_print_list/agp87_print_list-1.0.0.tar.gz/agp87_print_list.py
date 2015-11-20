def print_lol(the_list):
	for current_list_item in the_list:
		if isinstance(current_list_item,list) :
			print_lol(current_list_item)
		else:
			print(current_list_item)