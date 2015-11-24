#!/usr/bin/env python

from multiprocessing.dummy import Pool as thread_pool

def multiThread(threads=10):
    def __multiThread(func):
        def threadedFunc(iterable):
            pool = thread_pool(threads)
            for x in pool.map(func, iterable): yield x
        return threadedFunc
    return __multiThread
