# coding=utf-8
from  printtable import PrintTable    

table = PrintTable(['name','old'])
table.append_data(name = "小明",old = "20")
table.append_data(name =["小华","大傻"], old =["20","19"])
table.append_data_list(["二傻子","20"]) 

print "The table with line number\n"   
table.printTable(1)

print "The table without line number\n"   
table.printTable()
