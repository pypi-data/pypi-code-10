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

def printList(theList, indent=False, listSpace=0) :

	"""

		Esta função tem um argumento chamado "theList"
		que é qualquer lista python. Cada lista de dados
		fornecida na lista sera impressa na sua propria
		linha.
		
		Adicionado o argumento "listSpace" e definido seu
		valor padrão como "0", para imprimir tabulações de
		cada lista.
		
		Adicionado o argumento "indent" e definido seu valor
		padrão para "False" desta maneira ficando a criterio
		do programador utilizar a tabulação ou não. 
		
		"""

	for eachList in theList :
		if isinstance(eachList, list) :
			printList(eachList, indent, listSpace+1)
		else :
			if indent :
				for tab in range(listSpace) :
					print("\t"*listSpace, end='')
			print(eachList)
