"""define a function"""
def print_lol(the_list):
    """display each item in every lists"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)
