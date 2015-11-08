# -*- coding: utf-8 -*-
"""
pirnt nested list 

"""

def print_x(x, intend = False,level=0):
    for itemx in x:
        if isinstance(itemx,list):
            print_x(itemx,intend,level+1)
        else:
            if intend:
                for tab_stop in range(level):
                    print("\t",end='')
            print(itemx)


            