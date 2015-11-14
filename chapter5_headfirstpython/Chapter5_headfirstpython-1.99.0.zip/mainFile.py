
import sanitize


clean_james =[]
clean_julie =[]
clean_mikey = []
clean_sarah= []
with open('james.txt') as jams:
    data = jams.readline()
james = data.strip().split(',')

with open('julie.txt') as juls:
    data = juls.readline()
julie = data.strip().split(',')

with open('mikey.txt') as miks:
    data = miks.readline()
mikey = data.strip().split(',')

with open('sarah.txt') as sars:
    data = sars.readline()
sarah = data.strip().split(',')

try:
    for each_t in james:
        clean_james.append(sanitize.sanitze(each_t))
    for each_t in julie:
        clean_julie.append(sanitize.sanitze(each_t))
    for each_t in mikey:
        clean_mikey.append(sanitize.sanitze(each_t))
    for each_t in sarah:
        clean_sarah.append(sanitize.sanitze(each_t))
except IOError as err1:
    print('ERROR '+str(err1))


print(sorted(clean_james))
print(sorted(clean_julie))
print(sorted(clean_mikey))
print(sorted(clean_sarah
))



