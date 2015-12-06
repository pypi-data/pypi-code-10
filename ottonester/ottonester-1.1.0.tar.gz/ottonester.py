# This is a function for iterating through a list that may contain multiple layers of lists

def print_lol(the_list, level):
	# Pass the list, possibly containing nested lists to the function through the_list
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item, level+1)
		else:
			for tab_stop in range(level):
				print("t", end=' ')
			print(each_item)