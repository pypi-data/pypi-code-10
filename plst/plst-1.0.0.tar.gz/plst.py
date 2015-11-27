# -*- coding:utf-8 -*-

'''

		Este é o modulo "printList.py" ele fornece uma
		função onde pode ou não imprimir uma ou varias
		listas aninhadas.
		
		@Author: Jimmie Haskell
		@Date 27/11/2015
		@email: haskell4228@gmail.com	
			
'''

def printList(theList) :

#		Esta função tem um argumento chamado "theList"
#		que é qualquer list python. Cada lista de dados
#		fornecida na lista sera impresso na sua propria
#		linha.

	for eachList in theList :
		if isinstance(eachList, list) :
			printList(eachList)
		else :
			print(eachList)
