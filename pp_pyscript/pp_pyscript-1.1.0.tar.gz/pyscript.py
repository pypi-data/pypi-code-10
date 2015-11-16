"""I 
    love 
        u,
           my darlin"""

def print_lol(the_list,level):
    for each_1 in the_list:
        if isinstance(each_1,list):
            print_lol(each_1,level+1)
        else:
            for num in range(level):
                print('\t',end="")
            print(each_1)
if __name__ == '__main__':
    movie = ["Haixu Jin",
             "Leizhang Wang",
             "Pai Pang",
             ["1L1O1L",["Jian Ji","Shi Zigou", "Nan Dao"]],
             "Lingyu Zhang"]

    print_lol(movie,4)


 
            

