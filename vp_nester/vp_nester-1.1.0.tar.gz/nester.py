"""Este e o modulo "Nester.py", e fornece uma funcao chamada print_lol()
que imprime listas que podem ou nao incluir listas aninhadas"""

def print_lol(the_list, level):
    """ Esta funcao requer um argumento posicional chamado "the_list", que e
    qualquer lista python(de possiveis listas aninhadas). cada item de dado na
    lista fornecida e (recursivamente)impresso na tela em sua propria linha
    um segundo argumento chamada "level" e usado para inserir tabulacoes quando
    uma lista aninhada e encontada"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item,level+1)
        else:
            for tab_stop in range(level):
                print("\t", end='')
            print(each_item)
