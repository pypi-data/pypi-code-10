"""This prints all lists, including nested lists in a readable format.
Each data item is printed on its own line. A second argument called level
is used to create a tab-stop when a nested list is encountered."""

def print_list(the_list, level):
        for each_item in the_list:
                if isinstance(each_item, list):
                        print_list(each_item, level+1) #second argument increments level by 1
                else:
                    for tab_stop in range(level): #range is used to control how many tab-stop are needed
                        print("\t", end= ''"") #Displays a tab for each nested list and indents to denote the new nested list. '\' can not be the last character. Add "" to the end of the line to break out into a next line.
                    print(each_item)
