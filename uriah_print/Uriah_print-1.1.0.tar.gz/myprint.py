def print_list(myList, level = 0):
    for element in myList:
        if isinstance(element, list):
            print_list(element, level + 1)
        else:
            for i in range(level):
                print('\t', end = '')
            print(element)