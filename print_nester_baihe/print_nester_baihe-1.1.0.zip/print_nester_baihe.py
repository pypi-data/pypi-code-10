#!/usr/bin/env python
#coding:utf-8

'''这是\'nester.py\'模块，提供了一个名为print_lol()的函数，
这个函数的作用是打印列表，其中有可能包含（也可能不包含）嵌套列表。'''

from __future__ import print_function

def print_lol(m_list,indent=False,level=0):
  '''这个函数取一个位置参数，名为\'the_list\',这可以是任何
     python列表（也可以是包含嵌套列表或元祖的列表）。
     所指定的列表中每个数据项会（递归的）输出到屏幕上，各数据项占一行。'''
  for each_item in m_list:
      if isinstance(each_item, list):
          print_lol(each_item,indent,level+1)
      elif isinstance(each_item, tuple):
          print_lol(each_item,indent,level+1)
      elif isinstance(each_item, dict):
          print_lol(each_item,indent,level+1)
      else:
          if indent:
            for tab_stop in range(level):
              print ("  ", end=' ')
          print(each_item)
