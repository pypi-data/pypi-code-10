"""This is the test python for paulinus"""
def print_list(usr_list, indent=False, num=0):
    for each in usr_list:
        if isinstance(each, list):
            print_list(each, indent, num+1)
        else:
            if indent:
                for inter in range(num):
                    print("\t", end='')
            print(each)

