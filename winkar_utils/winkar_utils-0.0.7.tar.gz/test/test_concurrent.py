#!/usr/bin/env python

import unittest
from utils.concurrent import multiThread
import time

class concurrentTest(unittest.TestCase):
    def test_multiThread(self):
        @multiThread(10)
        def ox(x):
            return x

        linput=range(10)
        for k,res in enumerate(ox(linput)):
            self.assertEqual(linput[k],res)

if __name__=="__main__":
    unittest.main()
