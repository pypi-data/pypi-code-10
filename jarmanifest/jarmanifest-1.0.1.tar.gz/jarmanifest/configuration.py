import configparser
import os

def getConfig(filename):
	config = configparser.ConfigParser()
	config.readfp(open(filename))
	return config

config = getConfig('jarmanifest.cfg')
