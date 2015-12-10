"""This is the standard way to insert a multiple-line comment in your code."""
"""This module is my first sample edited by phyton"""
def print_kkk(the_list):
        """This module is to print out a complex list"""
        for each_list in the_list:
                if isinstance(each_list,list):
                        print_kkk(each_list)
                else:
                        print(each_list)
