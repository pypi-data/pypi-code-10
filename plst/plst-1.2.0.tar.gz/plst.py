# -*- coding:utf-8 -*-

'''

		Este é o modulo "printList.py" ele fornece uma
		função onde pode ou não imprimir uma ou varias
		listas aninhadas.
		
		@Author: Jimmie Haskell
		@Date 27/11/2015
		@email: haskell4228@gmail.com	
			
'''

from __future__ import print_function

def printList(theList, listSpace=0) : # adicionado o argumento "listSpace" e definido o valor padrão "listSpace=0"
	for eachList in theList :
		if isinstance(eachList, list) :
			printList(eachList, listSpace+1)
		else :
			for tab in range(listSpace) :
				print("\t", end='')
			print(eachList)
