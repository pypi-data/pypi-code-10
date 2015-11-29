#file that contains functions for parsing data structures

#takes a python list in string form and returns the list object back
def to_list(string):
    assign = 'lst = ' + string
    exec(assign)
    return locals()['lst']

def to_tuple(string):
    assign = 'tup = ' + string
    exec(assign)
    return locals()['tup']

def to_set(string):
    assign = 'ste = ' + string
    exec(assign)
    return locals()['ste']

def to_dict(string):
    assign = 'dict = ' + string
    exec(assign)
    return locals()['dict']

def to_obj(string):
    assign = 'obj = ' + string
    exec(assign)
    return locals()['obj']

def parse_data(string):
    import re
    obj_pat = [r"^\[.*\]$", r"^\{.*\}$", r"^\(.*\)$", r"^\{.*:.*,?\}$"]
    if re.match(r"^[0-9]+$", string):
        return int(string)
    else:
        for elem in obj_pat:
            if re.match(elem, string):
                return to_obj(string)
        return string