"""This is the test python for paulinus"""
def print_list(usr_list):
    for each in usr_list:
        if isinstance(each, list):
            print_list(each)
        else:
            print(each)

