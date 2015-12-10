"""Prints out Nested Lists"""

def print_lol(the_list, level=0):
        for an_entry in the_list:
                if isinstance(an_entry, list):
                        print_lol(an_entry, level+1)
                else:
                        for numTabs in range(level):
                                print("\t", end='')
                        print(an_entry)


                        
