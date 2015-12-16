"""这是我的学习测试模块,print_lol()函数
    test"""
def print_lol(the_list,indent=False,level=0):
    """你好这是测试模块
    test"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,indent,level+1)
        else:
            if indent:
                print("\t" * level,end="")
            print(each_item)
