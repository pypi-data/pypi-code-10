"""This is the standard way to insert a multiple-line comment in your code."""
"""This module is my first sample edited by phyton"""
def print_kkk(the_list, indent = False, level=0):
        """This module is to print out a complex list"""
        for each_list in the_list:
                if isinstance(each_list,list):
                        print_kkk(each_list, indent, level+1)
                else:
                        if indent:
                                for tab_step in range(level):
                                        print("\t", end='')
                        print(each_list)
