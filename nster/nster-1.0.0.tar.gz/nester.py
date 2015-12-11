def print_lol(the_list):
    for each_ietm in the_list:
        if isinstance(each_ietm,list):
             print_lol(each_ietm)
        else:
            print(each_ietm)
            
        
