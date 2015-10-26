def print_list(test, level):
    for element in test:
        if isinstance(element, list):
            print_list(element, level + 1)
        else:
            for num in range(level):
                print("\t", end='');
            print(element)