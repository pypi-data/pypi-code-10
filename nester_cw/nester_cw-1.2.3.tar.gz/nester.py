"""
This module aims to solve the nested items.
"""



def print_lol(the_list,level):
        """This funciton take one pareameter, named the_list,
        it could be anylist in python(it could be the one that contain nested list). Each item in the list take up one line and will be printed into screen.

"""

        for each_item in the_list:
		if isinstance(each_item, list):
                        print_lol(each_item,level+1)
		else:
			for tab_stop in range(level):
				print("\t", end = '')
        print(each_item)
                        
