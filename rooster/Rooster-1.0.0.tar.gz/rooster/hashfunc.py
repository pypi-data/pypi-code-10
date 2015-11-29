#file that contains hashing algorithm for file retrieval

class infinitelist(object):
    #allows a list to be accessed infinitely, where indexes beyond it's length are reduced to match an index.
    def __init__(self, lst):
        self.lst = lst
    def __repr__(self):
        return str(self.lst)
    def __len__(self):
        return len(self.lst)
    def __getitem__(self, i):
        if i == len(self.lst):
            return self.lst[i%len(self.lst)]
        elif i > len(self.lst)-1:
            return self.lst[i%len(self.lst)-1]
        else:
            return self.lst[i]
#converts a letter sequence into an integer
def name_to_int(string):
    import re
    string = string.lower()
    patterns = [r'a', r'b', r'c', r'd',
    r'e', r'f', r'g', r'h', r'i', r'j', r'k', r'l', r'm',
    r'n', r'o', r'p', r'q', r'r', r's',
    r't', r'u', r'v', r'w', r'x', r'y', r'z', r' ']
    numbers = [str(elem) for elem in range(1, 28)]
    for i in range(len(patterns)):
        string = re.sub(patterns[i], numbers[i], string)
    return int(string)

  #hashs an integer
def num_hash(i):
    chars = ['a', 'b', 'c', 'd',
    'e', 'f', 'g', 'h', 'i', '4', 'j', 'k', 'l', 'm',
    'n', 'q', 'o', 'r', 's',
    't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2',
    '3', '5', '6', '7', '8', 'p', '9']
    selection = infinitelist([x+y for x in chars for y in chars])
    hashed = ''
    while len(hashed) < 16:
        if i % 2 == 0:
            hashed += selection[i]
            i *= 4
        elif len(hashed) % 2 == 0:
            hashed += selection[i+4]
            i *= 3
        else:
            hashed += selection[i+1]
            i += 8
    return hashed

def do_hash(elem):
    elem = name_to_int(elem)
    return num_hash(elem)