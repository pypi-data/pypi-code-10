"""This is a python comment"""
def print_lol(the_list,level):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,level+1)
        else:
            for tab in range(level):
                print("\t",end='')
            print(each_item)
#this is also a python comment
