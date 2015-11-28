def print_lol(the_list,indent=false,level=0):
	"""This function takes one positional argument called "the_list", which is any
	Python list """
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,level+1)
		else:
			if indent:
				for tab_stop in range(level):
					print "\t" , "1"
				print(each_item)
