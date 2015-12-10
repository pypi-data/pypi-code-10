def print_lol(the_list,true_false=True,level=0):
    for listt in the_list:
        if isinstance(listt,list):
            print_lol(listt,true_false,level+1)
        else:
            if true_false:
                for ketim in range(level):
                    print("\t",end="")
            print(listt)
