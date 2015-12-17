"""
This is my string parser
This function will list all string in list recursively
"""

def list_string(my_list, level) : 
    for each_object in my_list :
        if isinstance(each_object, list) == True : 
            nester(each_object, level + 1)
        else : 
            for each_tab in range(level) :
                print("    ", end='');
            print(each_object);
