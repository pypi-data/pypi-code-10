"""Dies ist das Modul "entschachtler_mr.py". Es stellt eine Funktion namens print_lvl(),
die eine Liste mit beliebig vielen eingebetteten Listen ausgibt"""


def print_lvl(liste, einzug = True, ebene=0):
    for x in liste:
        if isinstance(x,list):
            print_lvl(x, einzug, ebene+1)
        else:
            if einzug == True:
                for tab in range(ebene):
                    print("\t", end='')
            print(x)