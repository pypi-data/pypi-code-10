'''
heartmath() function is a exam that straight out of ten math problems
each math problem contains three numbers are two integers even add operation
'''
import random
import time

# This is a function of the timer
def dur(op=None, clock=[time.time()]):
    if op != None:
        duration = time.time() - clock[0]
        print('%s finished. Duration %.6f seconds.' % (op, duration))
    clock[0] = time.time()
# This is a exam function
def heartmath():
    while True:
        reply = input('Enter text:')
        if reply == 'q':
            break
        elif not reply.isdigit():
            print('Bad!' * 8, reply.upper())
        else:
            print("Welcome to Numeric World!")
            dur()
            for item in range(10):
                a=random.randint(10,100)
                b=random.randint(10,100)
                c=random.randint(10,100)
                while True:
                    print((a),"+",(b),"+",(c),"=",)
                    result = input()
                    if not result.isdigit():
                        print("What?", d.upper(), 'It is String.')
                    elif int(result)==a+b+c:
                        print("Yes!")
                        break
                    else:
                        print("No!Try again.")
            dur('Well Done!')
    print("Bye!")