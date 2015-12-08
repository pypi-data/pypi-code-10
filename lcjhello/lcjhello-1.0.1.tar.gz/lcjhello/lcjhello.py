#!/bin/env python
#coding:utf-8

import getopt
import sys
def test(num):
	print num

def main():
	options, args = getopt.getopt(sys.argv[1:], ["help"])
	test(args)

if __name__ == '__main__':
	main()



