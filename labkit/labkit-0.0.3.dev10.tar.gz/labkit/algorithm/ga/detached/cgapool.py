#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

"""
Usage:

    tmpelate.py  [-q | --quiet] [-l | --log] [-d | --debug]
    tmpelate.py (-h | --help)
    tmpelate.py --version

Options:
    -h --help     Show this screen.
    --version     Show version.
    -l --log      Logging in makemd.log file.
    -q --quiet    Quiet output.
    -d --debug    Debug output.

Notes:
   my tmpelate
"""
from docopt import docopt
import os, sys, re, sh
from glob import glob
import yaml, logging

import mypub, labkitpath
import crash_on_ipy
import mylog



def load_config(filename='cga.config',mode='r'):
    """
    A config file sample. using yaml.
    output_type_list:
       - latex_article
       #- latex_report
       #- rtf
       #- docx
   """

    try:
        main_config=yaml.load(open(filename,mode))
    except Exception, e:
        return {}
    if not main_config:
        main_config={}
    return main_config

from



class Cgapool():
    
    def prepare_input_files(self,in_conformer):
        sh.mkdir(in_conformer)
        if in_conformer.calc_method=='xru_ga':
            in_conformer.get('in')['']

    def collect_output_files(self,in_conformer):
        sh.
    def run(self,in_conformer):
        '''

        :param in_conformer:
        :return:out_collection
        '''
        self.prepare_input_files()

        sh.xru_ga()
        self.collect_output_files()

        out_collection
        return out_collection

    def __init__(self,config_file):
        #read from config_file
        config=load_config("cga.config")
        #init conformer object
        self.pool=Pool(confog)
        self.pool.run()


    def run(self):
        #read from config_file
        pass

def cga():


    gapool=Cga(config_file)
    # gapool.init(config_file)
    gapool.run()





def main(logger=mylog.default_logger()):
    arguments = docopt(__doc__, version='0.0')
    self_name = os.path.basename(sys.argv[0])
    # logfile=self_name.replace('py','log')
    # logger=set_mylogger(arguments,logfile)
    # main_config=load_config('.ll')

    # dir_name=os.path.basename(os.getcwd())
    # test_file_name='test.txt'
    # test_file=open(test_file_name, 'w')
    # test_file.close()







if __name__ == '__main__':
    main()


