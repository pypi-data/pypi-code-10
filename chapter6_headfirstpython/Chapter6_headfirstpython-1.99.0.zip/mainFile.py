#this is mainFile.py for Chapter 6 of HeadFirst Python description "BUNDLING DATA"
#first project is to incorporate list into a dictionary

def sanitize(the_string):
    if '-' in the_string:
        splitter='-'
    elif ':' in the_string:
        splitter=':'
    else:
        return(the_string)
    (mins, sec) = the_string.split(splitter)
    return(mins+'.'+sec)

def load_coachData(Filename):
    try:
        with open(Filename) as data:
            mainData = data.readline()

        return(mainData.strip().split(','))
    except FileExistsError as err:
        print('ERROR FileExistError: '+str(err))

mikey = load_coachData('mikey2.txt')
sarah=load_coachData('sarah2.txt')
julie=load_coachData('julie2.txt')
james = load_coachData('james2.txt')


def data_dictionary(data_list):
    the_dict = {}
    the_dict['Name'] = data_list.pop(0)
    the_dict['DOB'] = data_list.pop(0)
    the_dict['timings'] = data_list

    return(print(the_dict['Name']+"'s fastest time is: "+str(sorted(set([sanitize(t) for t in data_list]))[0:3])+"BORN ON: "+the_dict['DOB']))


try:
    
    data_dictionary(mikey)
    data_dictionary(sarah)
    data_dictionary(julie)
    data_dictionary(james)
except IOError as err:
    print('ERROR no: '+str(err))
except ValueError as err:
    print('ERROR no: '+str(err))





