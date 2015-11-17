"""I 
    love 
        u,
           my darlin"""
import sys
def print_lol(the_list,indent=False,level=0, fn=sys.stdout):
    for each_1 in the_list:
        if isinstance(each_1,list):
            print_lol(each_1,indent,level+1, fn)
        else:
            if (indent == True):
                for num in range(level):
                    print('\t',end="", file = fn)
            print(each_1, file = fn)
if __name__ == '__main__':
            movie = ["Haixu Jin",
                    "Leizhang Wang",
                     "Pai Pang",
                     ["1L1O1L",["Jian Ji","Shi Zigou", "Nan Dao"]],
                     "Lingyu Zhang"]

            print_lol(movie,0)
            print_lol(movie,True,0)
            try:
               with open('mytest.txt','w') as out:
                    print_lol(movie,True,1,out)
            except IOError as err:
               print('err'+str(err)) 


 
            

