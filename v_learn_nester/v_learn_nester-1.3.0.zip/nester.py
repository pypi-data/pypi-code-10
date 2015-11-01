'''
This is the standard way to
include a multiple-line comment in
your code.
'''

def print_lol(the_list,indent = false,level = 0):
    '''
    This is a standard comment to the function
    '''
    for each_item in the_list:
        if isinstance (each_item,list):
            print_lol(each_item,indent,level+1)
        else:
            if indent:
                print('\t' * level,end='')
            print(each_item)
