#! /bin/user/env python
# -*- coding: utf-8 -*-
# 常用工具包
#filename: nester.py
#python35
#version: 1.2.0
'''A simple printer of nested lists
'''
#递归遍历多层列表
def printLoop(myList,indent = False, level = 0):
	for eachItem in myList:
		if isinstance(eachItem,list):
			printLoop(eachItem, indent, level + 1)
		else:
			if indent:
				for tab_stop in range(level):
					print("\t",end='')
			print(eachItem)
