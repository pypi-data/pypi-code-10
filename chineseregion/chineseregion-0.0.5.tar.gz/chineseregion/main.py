# -*- coding: utf-8 -*-
__author__ = 'xuanwo'

'''
chineseregion cli

Usage:
    chineseregion "your position"
'''

import os, sys
import json
import pkgutil
import chineseregion
from pkg_resources import resource_string

# data = json.loads(str(pkgutil.get_data(chineseregion.__package__, 'data.json'),'utf-8'))
data = json.loads(str(resource_string(__name__, 'data.json'),'utf-8'))

def find(str):
    city = []
    for i in sorted(data.keys()):
        if str.find(data[i]) != -1:
            city.append(data[i])
    return city


def main():
    argv = sys.argv[1:]
    for i in argv:
        ans = find(i)
        if len(ans) != 0:
            print(ans)
        else:
            print("Not Found")


if __name__ == "__main__":
    main()
