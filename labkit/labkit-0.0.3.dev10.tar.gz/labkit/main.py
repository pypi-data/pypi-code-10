#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

from sigtools.modifiers import kwoargs
from clize import run

from labkit import check_config
from labkit.algorithm.ga.cga import cga_run
from labkit.algorithm.sys import cga




def main():
    # 循环config

    for turn in check_config.RUN:
        SAMPLE_METHOD = turn['SAMPLE_METHOD']
        algorithm = turn['SAMPLE_METHOD']['ALGORITHM']
        constraned = turn['SAMPLE_METHOD']['CONSTRANED']
        meta_method = turn['META_METHOD']

        if algorithm == 'SYS':
            cga_run()
        elif algorithm=='GA':
            cga_run()





if __name__ == '__main__':
    run(main)
