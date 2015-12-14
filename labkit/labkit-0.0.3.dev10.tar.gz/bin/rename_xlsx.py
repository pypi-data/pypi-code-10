#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


from xlrd import open_workbook
# from xlutils.copy import copy
import os,re


def format_to_xyz(filename):
    filename = str(filename)
    filename = filename.replace('.xyz', '')
    filename = filename.replace('.out', '')
    filename = filename + '.xyz'
    return filename


def main():
    if os.system("ls|grep \.out|while read i;do out-xyz $i&&rm $i;done"):
        exit(0)
    xlsx_file_name = filter(lambda s:re.findall(r'^[^\~].*\.xlsx?$',s),os.listdir('.'))[0]


    data = open_workbook(xlsx_file_name)
    table = data.sheets()[0]

    # data_for_write = copy(data)
    # table_for_write = data_for_write.get_sheet(0)

    nrows = table.nrows
    ncols = table.ncols
    curpath = os.curdir

    for i in range(1, nrows):
        before = str(table.cell(i, 0).value).replace('.0','')
        after = i

        before_file_name = os.path.join(curpath, format_to_xyz(before))
        after_file_name = os.path.join(curpath, format_to_xyz(after))

        os.rename(before_file_name, after_file_name)
        # row = i
        # col = 0
        # ctype = 1  # 类型 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
        # value = after
        # xf = 0  # 扩展的格式化 (默认是0)
        # table_for_write.write(row, col, value)
    os.system("open %s" % xlsx_file_name)

    # data_for_write.save(xlsx_file_name)

if __name__ == '__main__':
    main()
