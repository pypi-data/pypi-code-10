"""
	Function to deserialize the file config
"""
	
import configparser
import os

def get_config(file):
    config = configparser.ConfigParser()
    myPath=os.path.dirname(os.path.dirname(file))
    myFile=myPath+'\\config.ini'
    config.read(myFile)
    return config