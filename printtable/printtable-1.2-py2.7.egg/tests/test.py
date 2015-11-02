from printtable import PrintTable

table = PrintTable(['name','old'])
table.append_data(name="Jack",old = "20")
table.append_data(name =["Jack","Mary"], old =["20","19"])
table.append_data_list(["Jack","20"]) 

print "The table with line number\n"   
table.printTable(1)

print "The table without line number\n"   
table.printTable()
