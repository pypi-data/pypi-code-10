__author__ = 'floyd'
""" Apenas uma definição simples para impressão de listas aninhadas com o único propósito
    de seguir o proposto no livro headfirst Python
    """
def print_lol(the_list, ident=False, level=0):
    #prints a list of possibily nested lists
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, ident,level+1)
        else:
            if ident:
                for tab_stop in range(level):
                    print("\t",end='')
            print(each_item)