#!/usr/bin/env python

from primefac import primefac

def factor(n):
    res =  [x for x in primefac(n)]
    if len(res)==1:
        res= [1] + res
    return res

if __name__=="__main__":
    import sys
    n = int(sys.argv[1])
    print "%d:"%n,
    for x in factor(n):
        print x,
