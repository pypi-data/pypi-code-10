def hhhh(opp,indent=False,level=0):
        for yuansu in opp:
                if isinstance(yuansu,list):
                        hhhh(yuansu,indent,level+1)
                else:
                        if indent:
                                for tab_ii in range(level):
                                        print("\t",end='')
                        print(yuansu) 
