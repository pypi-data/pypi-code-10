"""This is a python comment"""
import sys
def print_lol(the_list,indent=False,level=0,fh=sys.stdout):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,indent,level+1,fh)
        else:
            if indent:
                for tab in range(level):
                    print("\t",end='',file=fh)
            print(each_item,file=fh)
#this is also a python comment
