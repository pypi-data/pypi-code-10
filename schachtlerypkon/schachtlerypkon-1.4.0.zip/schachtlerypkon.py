import sys
"""Ein Modul um alle Einzeldaten einer Liste anzuzeigen"""
def print_lvl(liste,einzug=False, ebene=0, dat= sys.stdout):
    """Mit dieser Funktion wird sichergestellt, dass auch in Listen eingebettete Listen
    einzeln dargestellt werden (die normale Tiefe beträgt bis zu 1000 Ebenen.
    Die Funktion erwartet ein positionelles Argument namens "liste", das eine beliebige Python-Liste ist.
    Wenn du das dritte Argument nutzen möchtest setze einzug=True.
    Mit Hilfe des dritten Arguments wird angezeigt wenn eine liste in einer liste eingebettet ist.
    Um anzugeben, wohin print_lvl die Daten schreibt kann man nun ein drittes Argument angeben, standardmäßig hierfür bleibt aber die Ausgabe auf den Bildschirm"""

    for element in liste:
        if isinstance(element, list):
            print_lvl(element,einzug, ebene+1,dat)
        else:
            if einzug:
                for tab in range(ebene):
                    print("\t", end='',file=dat)
            print(element,file=dat)        
