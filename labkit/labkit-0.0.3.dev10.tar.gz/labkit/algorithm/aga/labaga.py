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

import mypub,labkitpath
import crash_on_ipy
import mylog



class AGA():


    def run(self,initial_conformer):

        loop_conformer=initial_conformer
        converged_flag=20
        while not converged_flag:
            self.ga(loop_conformer,ga_collection,force_field)  # 400代
            low_collection=self.lowconf(ga_colletion) # 提取前10
            # self.aga_pool.add(ga_pool) # 收集进agapool
            self.aga_qm(low_collection,qm_collection)
            self.fit(low_collection,ga_collection)
            self.qm_pool.add(qm_collection)
            loop_conformer=lowest_conformer
            converged_flag=converged_flag-1

        self.lowconf(qm_pool)
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


