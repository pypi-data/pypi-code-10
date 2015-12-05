#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import sys
import argparse
import re
import sys
import select

WHITE = "\033[0m"
#gris = "\033[0;37m"
#magenta = "\033[0;35m"
RED = "\033[1;31m"
GREEN_2 = "\033[1;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
#cyano = "\033[1;36m"
#rescolor = "\e[0m"
GREEN = '\033[92m'

def set_color(patron, color, texto):
    
    setcolor = r'%s\1%s' %(color, WHITE)    
    texto_color = re.sub(patron, setcolor , texto)
    return texto_color

def main():

    


    pattern_email = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                        "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                        "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))

    pattern_ip = r"((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)([ (\[]?(\.|dot)[ )\]]?(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3})"
    #for line in sys.stdin:
        #sys.stdout.write(line)
    #import sys
    #data = sys.stdin.readlines()
    
    #print data
    
    parser = argparse.ArgumentParser( 
        description="""Ejemplo 1: #cat log.txt | sw  ,  Ejemplo 2: #sw log.txt""",
        epilog='Aplicar colores email y ip'
    )
    #parser.add_argument("-h", "--help", help="Ejemplo: cat log.txt | sw ")
    #parser.add_argument("-v", "--verbose", help="Mostrar información de depuración", action="store_true")
    #parser.add_argument("-f", "--log", help="Archivo de texto")

    
    

    pipe = select.select([sys.stdin,],[],[],0.0)[0]
    
    if pipe:
        #print "Have data!"

        
        

       

        tuberia = sys.stdin.read()

        archivo_open = set_color(pattern_email, GREEN, tuberia)
        archivo_open = set_color(pattern_ip, YELLOW, archivo_open)

        # patron = r'%s\1%s' %(GREEN, blanco)    
        # archivo_open = re.sub(pattern_email, patron , tuberia)
        
        # patron = r'%s\1%s' %(azul, blanco)    
        # archivo_open = re.sub(pattern_ip, patron , archivo_open)

        print archivo_open

    else:
        #print "No data"
        #pass

        parser.add_argument("echo")
        args = parser.parse_args()

        if args.echo:
            archivo_open = None
            try:
                archivo = open(args.echo, "r")
                archivo_open = archivo.read()
                archivo.close()                
                
            except Exception, e:
                raise e

            if archivo_open:
                archivo_open = set_color(pattern_email, GREEN, archivo_open)
                archivo_open = set_color(pattern_ip, YELLOW, archivo_open)
                print archivo_open
                







    # if not sys.stdin.isatty():
    #     print "not sys.stdin.isatty"
    # else:
    #      print "is  sys.stdin.isatty"

    # while 1:
    #     try:
    #         line = sys.stdin.read()
    #     except KeyboardInterrupt:
    #         break

    #     if not line:
    #         break

    #     print "run"

    #     patron = r'%s\1%s' %(GREEN, blanco)
    
    #     archivo_open = re.sub(pattern_email, patron , line)

    #     print archivo_open

    # parser = argparse.ArgumentParser()
    # parser.add_argument("-v", "--verbose", help="Mostrar información de depuración", action="store_true")
    # parser.add_argument("-f", "--log", help="Archivo de texto")
    # args = parser.parse_args()
    
    # pattern = r"((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)([ (\[]?(\.|dot)[ )\]]?(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3})"
    # #ips = [each[0] for each in re.findall(pattern, line)]
    
    
    
    # if args.verbose:
    #     print "depuracion activada!!!"
    
    
    # if args.log:
    #     try:
    #         archivo = open(args.log, "r")
    #         archivo_open = archivo.read() 

    #         # for linea in archivo.readlines():    
    #         #     ips = [each[0] for each in re.findall(pattern, linea)]
    #         #     emails = [each[0] for each in re.findall(pattern_email, linea)]
    
    #         #     for ip in ips:
    #         #         #print ip
    #         #         ipcolor= set_color(amarillo, ip)
    #         #         linea = linea.replace(ip,ipcolor,1)
    
    #         #     for email in emails:
    #         #         emailcolor= set_color(GREEN, email)
    #         #         linea = linea.replace(email,emailcolor,1)

    #         patron = r'%s\1%s' %(GREEN, blanco)
    #         #archivo_open = re.sub(pattern, r'\033[92m\1\033[0m', archivo_open)
    #         archivo_open = re.sub(pattern_email, patron , archivo_open)
            
    #         print archivo_open
                
    
    #             #linea = re.sub(pattern, ".",linea)
    #             #print linea.strip()
                
    #         archivo.close() 
    #     except Exception, e:
    #         raise e


if __name__ == '__main__':
    main()







