#This is the mainFile.py,a program which will a run a simple test of saving a file into a disk

#this import.os is used to invoke the Standard Library of OS which is reading,saving and editing files or even locating them
import os
import nester

#this getcwd() method is used to check the Current working directory, which is the file that im using right now at C:
#getcwd() can only be used once the OS library has been imported to the program
#to change the directory, you can use the os.chdir()
os.getcwd()


man = []#null list
other = []#null list

#what this program will do, is read all the text inside the 'sketch.txt' file and then process the values inside the string
try:
    #opening a file
    data = open('sketch.txt')
    try:
        for each_line in data: #reading all the lines in the sketch.text file using a for loop
            (role, line_spoken) = each_line.split(':', 1)#split each line into variables, the first variable is assigned to role, thesecond one is to 'line_spoken', the split will only happen if the program encounters a colon ONCE
            line_spoken = line_spoken.strip()#line_spoken.strip() will do is to remove the white spaces and the '\n" from the strings
            if role == 'Man':#everytime the first identifier(role) hits 'Man' Dialogue it stores its values to the empty list man[]
                man.append(line_spoken)
            elif role== 'Other Man':
                other.append(line_spoken)#everytime the first identifier(role) hits 'Other man' Dialogue it stores its values to the empty list other[]
        data.close()#closing the data object
    except ValueError:
        pass#exception passed
except IOError as err2:
    print('Error no.2'+str(err2))#checks wether the file exist

"""This lines of codes will fetch the data from man[] list now that it has a value, the value from each list(man[],other[]) will now
be processed and stored(persistence) in a file called man_file.txt, and other_file.txt, both of which will store the line_spoken from the two
list.
"""
try:
    #to create a new file you must use the 'w' access mode from the open() method, this will allow the creation of a file
    #using 'WITH' keyword, theres no need to use 'FINALLY', but it must only be used when creating data
    with open('man_file.txt', 'w') as man_data, open('other_file.txt','w') as other_data:
        print(man, file=man_data)#assigning the data to be stores in the file
        print(other,file=other_data)
except IOError as err3:
    print('Error no 3'+str(err3))#exception handling


with open('man_file.txt') as mdf:
    nester.print_lol(mdf.readline())