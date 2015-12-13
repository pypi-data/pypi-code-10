#!/usr/bin/env python
# -*- coding:utf-8 -*


'''
	Un Sapin de Noel à base de 
		- Sapin
		- Raspberry pi
		- guirelande + relais
		- detecteur de mouvement IR
		- ...
'''
#Pour travailler sur les sources
import sys
sys.path.insert(0,'../FGPIO')
sys.path.insert(0,'../FUTIL')

#from FGPIO.relay_io import *
#from FGPIO.ir_detect_io import *
from FUTIL.my_logging import *

class sapin(object):
	'''Un Sapin de Noel avec une Raspberry dedans
	'''
	def __init__(self, guirelande = None, clignotte_on = 5, clignotte_off = 2, guirelande_RF = None, detecteur_ir = None):
		'''Initialisation
			- guirelande	:	FGPIO.relay_io
			- clignotte_on	:	Durée du clignottement "on" de la guirelande
			- clignotte_off	:	Durée du clignottement "off" de la guirelande
			- guirelande_RF :	Prise RF sur laquelle est branchee un guirelande qui clignote toutes seule
			- detecteur_ir	:	FGPIO.ir_detect_io
		'''
		self.guirelande = guirelande
		self.detecteur_ir = detecteur_ir
		self.clignotte_on = clignotte_on
		self.clignotte_off = clignotte_off
		self.guirelande_RF = guirelande_RF
		if self.detecteur_ir:
			self.detecteur_ir.add_thread(self.on_detecteur_ir_change)
		else:
			logging.debug("La guirelande va clignotter pour toujours")
			self.clignotte()
			
		
	def clignotte(self, marche = True):
		'''Fais clignotter indéfiniment la guirelande
			- marche	:	Si True		: débute le clignottement
							Si False	: stop le clignottement
		'''
		if self.guirelande:
			if marche :
				self.guirelande.blink(self.clignotte_on,self.clignotte_off)
			else:
				self.guirelande.stop()
	
	def clignotte_guirelande_RF(self, marche = True):
		'''Allume une guirelande branche sur une prise RF
		'''
		if self.guirelande_RF:
			self.guirelande_RF.set(marche)
		
	def on_detecteur_ir_change(self):
		'''Deamon quand le detecteur IR change d'état
		'''
		if self.detecteur_ir.th_readed():
			logging.debug("Detection de mouvement : la guirelande clignotte")
			self.clignotte()
			self.clignotte_guirelande_RF()
		else:
			logging.debug("Plus de mouvement : la guirelande stoppe")
			self.clignotte(False)
			self.clignotte_guirelande_RF(False)
	
	def stop(self):
		'''Stop tous les threads
		'''
		if self.guirelande:
			self.guirelande.stop()
		if self.detecteur_ir:
			self.detecteur_ir.stop()