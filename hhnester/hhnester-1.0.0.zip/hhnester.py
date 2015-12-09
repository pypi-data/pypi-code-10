def print_lol(this_list):
	for  e in this_list:
		if isinstance(e,list):
			print_lol(e)
				
		else:
			print(e)

			
