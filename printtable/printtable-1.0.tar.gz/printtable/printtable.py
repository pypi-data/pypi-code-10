#!/usr/bin/python2.7
# -*- coding: utf-8 -*-


class PrintTable(object):
    """draw the table in the terminal"""
    def  __init__(self, attribute):
        self.StrTable = ""
        self.Attribute = []
        self.Col_num = len(attribute)
        self.Row_num = 1
        self.AttributeLen = dict()
        self.table = dict()
        self.line_len = 0

        for attr in attribute:
            attr =  str(attr)
            self.Attribute.append(attr)
            self.table[attr] = [attr]
            self.AttributeLen[attr] = len(attr)+2

    def add_data(self,attr,value):
        """append list of data or a data in the table,
        this function is used by append_data() , not use Separately.

            for example:
                add_data("name","Jack")  or
                add_data("name",["Jack","Mary"])
        """
        tp = type(value)
        if tp == str:
            self.table[attr].append(value)
            self.AttributeLen[attr] = max(self.AttributeLen[attr],len(value)+2)
        elif tp == int:
            self.table[attr].append(str(value))
            self.AttributeLen[attr] = max(self.AttributeLen[attr],len(str(value))+2)
        elif tp == list:
            for v in value:
                self.table[attr].append(str(v))
                self.AttributeLen[attr] = max(self.AttributeLen[attr],len(str(v))+2)
        self.Row_num = max(self.Row_num, len(self.table[attr]))

    def append_data_list(self,value_lists):
        """append list of data in the table

            for example:
                append_data_list(["Jack","20"]) 
        """
        value_list = [str(vl) for vl in value_lists]
        for i in range(self.Col_num):
            if i < len(value_list):
                self.table[self.Attribute[i]].append(value_list[i])
                self.AttributeLen[self.Attribute[i]] = max(self.AttributeLen[self.Attribute[i]],len(value_list[i])+2)
            else:
                self.table[self.Attribute[i]].append("")
        self.Row_num+=1

    def append_data(self,**args):
        """append data with Keyword parameters in the table, 

        the premise is Keyword parameters in the attribute before.

            for example:
                append_data(name="Jack",old = "20") or
                append_data(name =["Jack","Mary"], old =["20","19"])
        """
        for attr in self.Attribute:
            if attr in args:
                self.add_data(attr,args[attr])
        for attr in self.Attribute:
            self.table[attr].extend(["" for i in xrange(self.Row_num-len(self.table[attr]))]) 

        
    def printDivide(self,line_num):
        """add separation in the Strtable

        Args:
            line_num: Add line numbers in front of each line, ,default 0.
        """
        if line_num == 1:
            self.StrTable += "+" + "-"*self.line_len

        for attr in self.Attribute:
            self.StrTable += "+"
            self.StrTable += "-"*self.AttributeLen[attr]
        self.StrTable += "+"+"\n"



    def  printTable(self,line_num=0):
        """Print table in console/terminal

        Args:
            line_num: Add line numbers in front of each line, ,default 0.
        """
        if line_num == 1:
            self.line_len = len(str(self.Row_num))+2

        self.StrTable=""
        self.printDivide(line_num)
        for num in xrange(self.Row_num):
            self.StrTable += "|"

            if line_num == 1:
                if num == 0:
                    self.StrTable += " "*self.line_len+"|"
                elif num>0:
                    space_num = (self.line_len-len(str(num)))/2
                    self.StrTable += " "*space_num+str(num)+" "*(self.line_len-len(str(num))-space_num)+"|"

            for attr in self.Attribute:
                space_num = (self.AttributeLen[attr]-len(self.table[attr][num]))/2
                self.StrTable += " "*space_num+self.table[attr][num]+\
                                         " "*(self.AttributeLen[attr]-len(self.table[attr][num])-space_num) + '|'
            self.StrTable += "\n"
            self.printDivide(line_num)

        print self.StrTable
