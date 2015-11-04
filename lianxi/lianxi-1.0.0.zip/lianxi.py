def ffffo(the_list):
    for yuansu in the_list:
        if isinstance(yuansu,list):
            ffffo(yuansu)
        else:
            print(yuansu)
