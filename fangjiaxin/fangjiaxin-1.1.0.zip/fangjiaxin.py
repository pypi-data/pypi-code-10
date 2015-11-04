'''this is a module'''
def print_lol(the_list,level): #the_list tells you the type of the input
    '''this is a list function''' #describe the function
    for each_item in the_list:            
        if isinstance(each_item,list):
            print_lol(each_item,level+1)
        else:
            for num in range(level):
                print "\t",str(each_item)
            
