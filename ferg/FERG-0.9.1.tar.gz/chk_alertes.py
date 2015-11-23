#!/usr/bin/env python
# -*- coding:utf-8 -*

####################################
'''
Lecture de la base de données des températures
Et envoie de mail si alerte.

Plus création des conso déduites.
'''
#################################### 

#Pour travailler sur les sources
import sys
sys.path.insert(0,'../FGPIO')
sys.path.insert(0,'../FUTIL')

import FERG.tempeDB
import FERG.installation
from FUTIL.my_logging import *
import FUTIL.mails

#TODO : A sécuriser : + redondant avec config.py 
MyMail = FUTIL.mails.gmail(gmail_account='xxx', gmail_pwd='xxx')


my_logging(console_level = INFO, logfile_level = INFO)

logging.info("Execution de chk_alertes.py")


# Gestion des températures
db = FERG.tempeDB.tempeDB(db_name="tempeDB", user="fred", passwd="achanger", host="192.168.10.10", mail = MyMail)
db.check_alertes()
db.chk_mesures()

#Gestion des consos electriques
import config
install = config.get_installation(physical_device = False)

install.deduit_conso_arithmetic()
install.deduit_conso_typiques()
install.check_alertes()
