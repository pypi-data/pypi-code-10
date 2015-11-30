def print_lol(a_list, level=0):

    for each_item in a_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1)
        else:
            for l in range(level):
                print("\t", end='')
            print(each_item)
