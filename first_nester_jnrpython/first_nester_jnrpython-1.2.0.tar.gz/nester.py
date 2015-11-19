# -*- coding: utf-8 -*-
"""Esta é o modulo "nester.py" e ele fornece uma função chamada print_lol() que imprime listas que 
podem ou não incluir listas aninhadas."""
def print_lol(the_list, level=0):
    """Essa funcao tem um argumento posicional chamado "the_list" que é uma lista Python qualquer (talvez aninhada). 
    Cada item   na lista fornecida é (recursivamente) imprimida na tela na sua própria linha. Um segundo argumento 
    chamado "level" é usado para inserir tab-stops quando uma lista aninhada é encontrada."""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1)
        else:
            for tab_stop in range(level):
                print("\t", end=" ")
            print(each_item)