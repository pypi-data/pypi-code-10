"""This module contains functions:
    1 . list_prime(ll,ul)  :: Returns a list of all prime numbers between integers ll and ul(both included)
    2 . rand_prime(ll,ul)  :: Returns a random prime number between integers ll and ul(both included)
    3 . is_prime(x)        :: Displays if entered number is prime or not """

from math import sqrt
from math import floor


def list_prime(a,b):     #Returns a list of all primes between a and b,both included
    l = []
    if a>=b:
        print "Error :: Wrong parameters entered: a<b"
    elif a!= floor(a) or b!= floor(b):
        print "Error :: Input must be non-negative integers"
    elif a<0 or b<0:
        print "Error :: Negative parameters entered"
    else:
        for i in range(a,b+1):
          ctr = 0 
          for j in range(2,int(sqrt(i))+2):
            if i%j==0:
               ctr+=1
            break
          if ctr == 0 or i == 2:
            l.append(i)
        return l
     

def rand_prime(a,b):     #Returns a random prime number from a specified range
    if a>=b:
        print "Error :: Wrong parameters entered: a<b"
    elif a!= floor(a) or b!= floor(b):
        print "Error :: Input must be an integer"
    elif a<0 or b<0:
        print "Error :: Negative parameters entered"
    else:
        import random
        while True:
           x = random.randint(a,b)
           ctr = 0 
           for i in range(2,int(sqrt(x))+2):
             if x%i==0:
              ctr+=1
              break
           if ctr == 0:
            return x
                
    

def is_prime(a):         #Displays whether entered number is prime or composite
    ctr = 0
    if a<=0:
        print "Error :: Invalid number entered"
    elif a != floor(a):
        print "Error :: Input must be a positive integer"
    elif a == 1:
        print "1 is neither prime nor composite"
    else:    
        for i in range(2,int(sqrt(a))+2):
           if a%i == 0:
              ctr+=1
              break
        if ctr == 0 or a == 2:
               print str(a)+" is prime"
        else:
               print str(a)+" is composite"
         

