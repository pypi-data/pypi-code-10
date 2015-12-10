"""Prints out Nested Lists"""

def print_lol(the_list, indent=True, level=0):
        for an_entry in the_list:
                if isinstance(an_entry, list):
                        print_lol(an_entry, indent, level+1)
                else:
                        if (indent):
                                
                                for numTabs in range(level):
                                        print("\t", end='')
                        print(an_entry)


                        
