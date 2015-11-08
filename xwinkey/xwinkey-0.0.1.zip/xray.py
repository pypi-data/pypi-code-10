# -*- coding: utf-8 -*-
"""
pirnt nested list 

"""

def print_x(x):
    for itemx in x:
        if isinstance(itemx,list):
            print_x(itemx)
        else:
            print(itemx)


            