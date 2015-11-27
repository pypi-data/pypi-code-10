#2015.11.20 61page
"""
This is the standard way to
include a multiple-line comment in
your code
"""
"""
Added Level term to tab space.
"""

"""movies = ["The Holy Grail", 1975, "Terry Jones & Terry Gilliam", 91,
              ["Graham Chapman", ["Michael Palin", "John Clese",
                    "Terry Gilliam", "Eric Idle", "Terry jones"]]]
"""

"""
def print_lol(the_list, level):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            for num in range(level):                
                print("\t",end=")
            print(each_item)
"""
#print_lol(movies)
# import sys; sys.path # Dispaly python autopath.

def print_lol(the_list, level=0):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item,level+1)
        else:
            for num in range(level):
                print("\t",end='')
            print(each_item)
    
