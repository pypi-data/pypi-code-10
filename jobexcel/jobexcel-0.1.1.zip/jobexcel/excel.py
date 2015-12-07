# -*- coding: UTF-8 -*-

import xlwt
import xlrd
from xlutils.copy import copy
import shutil
import os
import sys


class Excel(object):

    def __init__(self,filename):
        self.xlsname = filename
        self.target_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)),'result')
        self.robj = self._connect_excel()
        self.wobj = copy(self.robj)

    def _connect_excel(self):
        '''
        if the target file dose not exist,then create file named self.xlsname
        :param create_new:
        :return:workbook
        '''
        try:
            return xlrd.open_workbook(self.xlsname)
        except IOError:
            print 'sorry,but the target file dose not exist,please check the file path.'
            print 'if you want to create new file ,please use baseclass "WExcel"'
            sys.exit(0)

    def write(self,data):
        pass

    def sync(self,dest=None):
        # compared to move method,it can modify the existence file,but it only works in Linux
        if dest is None:
            dest = self.target_dir
        os.system('rsync -av %s %s'%(self.xlsname,dest))

    def save(self,savename=None,dest=None):
        if savename is None:
            savename = self.xlsname
        self.wobj.save(savename)
        if dest is None:
            dest = self.target_dir
        try:
            shutil.move(savename,dest)
        except shutil.Error:
            os.remove(os.path.join(dest,savename))
            shutil.move(savename,dest)


class WExcel(Excel):

    def __init__(self,filename,sheetnames=None):
        super(WExcel,self).__init__(filename)
        self.wobj = self._connect_excel()
        self._add_sheet(sheetnames)

    def _connect_excel(self):
        return xlwt.Workbook(encoding='utf8')

    def _add_sheet(self,names):
        if names is None:
            self.wobj.add_sheet('sheet1')
        elif isinstance(names, list):
            for sh in names:
                self.wobj.add_sheet(sh)
        elif isinstance(names,basestring):
            self.wobj.add_sheet(names)

    def write_title(self, data, sheetid=0):
        sheet = self.wobj.get_sheet(sheetid)
        al = xlwt.Alignment()
        al.horz = xlwt.Alignment.HORZ_CENTER
        al.vert = xlwt.Alignment.VERT_CENTER
        style = xlwt.XFStyle()
        style.alignment = al
        font = xlwt.Font()
        font.name = 'SimSun'
        font.height = 330
        font.colour_index = 33
        if isinstance(data,list):
            for index,value in enumerate(data):
                sheet.write(0,index,value,style)
        elif isinstance(data,dict):
            #here,key is col num
            for key in data.keys():
                sheet.write(0,int(key),data[key],style)
        else:
            print 'data must be tuple,list or dict'
            print type(data)

    def write(self, sheetid=0):
        pass





if __name__=="__main__":

    class T_Excel(Excel):

        def __init__(self,filename):
            super(T_Excel,self).__init__(filename)

        def write(self, sheetid=0):
            sheet = self.wobj.get_sheet(sheetid)
            sheet.write(1,30,'tests')


    t = T_Excel(u'tests.xls')
    t.write()
    t.save('s.xls')







