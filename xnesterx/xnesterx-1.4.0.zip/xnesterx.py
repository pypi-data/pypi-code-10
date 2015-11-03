'''Module to print the elements of a nested list'''
#levelspecifies the number of tabs
#False to to switch off indentation
import sys
#to use sys
#specify where you want to print the data using target_file argument
#By default it outputs to screen
def print_lol (the_list,indent=False,level=-7,fh=sys.stdout):
        for each_item in the_list:
                if isinstance(each_item,list):
                        print_lol(each_item,True,level+1,fh)
                else:
                        if indent:
                                for tab_stop in range(level):
                                        print("\t",end='',file=fh)
                        print(each_item,file=fh)
