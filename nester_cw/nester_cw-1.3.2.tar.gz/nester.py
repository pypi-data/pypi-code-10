"""
This module aims to solve the nested items.
"""


import sys
def print_lol(the_list,indent = False, level = 0,fh = sys.stdout):
        """This funciton take one pareameter, named the_list,
        it could be anylist in python(it could be the one that contain nested list). Each item in the list take up one line and will be printed into screen.

"""

        for each_item in the_list:
                if isinstance(each_item, list):
                        print_lol(each_item, indent, level+1,fh)
                else:
                        if indent:
                                for tab_stop in range(level):
                                        print("\t", end = '',file = fh)
                        print(each_item,file = fh)
                
