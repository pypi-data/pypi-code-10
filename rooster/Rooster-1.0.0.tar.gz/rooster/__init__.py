#file for creating the hash key-values
import os
import sys

from rooster.hashfunc import *
from rooster.parsedata import *


#creates a directory in python
def createrooster(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        raise FileExistsError("directory name already exists")
#sets a rooster key-value pair
def set_rooster(key, value, directory):
    try:
        hash_key = do_hash(key)
        hash_key += ".rooster"
        target = open(os.path.join(directory, hash_key), 'w')
        target.write(str(value))
        target.close()
    except FileNotFoundError:
        return "directory does not exist"
    except ValueError:
        return "key contains invalid characters, please use only alpha numeric or spaces"

#gets a rooster key-value pair
def get_rooster(key, directory):
    try:
        hash_key = do_hash(key)
        hash_key += ".rooster"
        target = open(os.path.join(directory, hash_key), 'r')
        value = target.read()
        target.close()
        return parse_data(value) #parses the value back into appropriate python data structure.
    except FileNotFoundError:
        return "key or directory does not exist"
    except ValueError:
        return "key contains invalid characters, please use only alpha numeric or spaces"

#strictly returns the string within the rooster storage file, without parsing it back into a data structure
def get_str_rooster(key, directory):
    try:
        hash_key = do_hash(key)
        hash_key += ".rooster"
        target = open(os.path.join(directory, hash_key), 'r')
        value = target.read()
        target.close()
        return value
    except FileNotFoundError:
        return "key does not exist"
    except ValueError:
        return "key contains invalid characters, please use only alpha numeric or spaces"

#checks if a key exists
def check_key(key, directory):
    hash_key = do_hash(key)
    hash_key += ".rooster"
    target = os.path.join(directory, hash_key)
    return os.path.exists(target)
#only sets a key if it does not overwrite current key.
def safe_set(key, value, directory):
    if check_key(key, directory):
        return "key already exists"
    else:
        set_rooster(key, value, directory)

#deletes a key-value entry from the hash-bucket returns true if successful.
def del_key(key, directory):
    hash_key = do_hash(key)
    hash_key += ".rooster"
    target = os.path.join(directory, hash_key)
    os.remove(target)
    return True

#takes a Python dictionary and saves the entire dictionary into seperate key-value buckets.
def set_dict(dict, directory):
    keys, values = list(dict.keys()), list(dict.values())
    for i in range(len(keys)):
        set_rooster(keys[i], values[i], directory)
    return True

#safe sets a python dictionary as seperate key-value buckets
def safeset_dict(dict, directory):
    keys, values = list(dict.keys()), list(dict.values())
    for i in range(len(keys)):
        safe_set(keys[i], values[i], directory)
    return True


#file open method for production, for debugging, use default open method.
def getScriptPath():
    return os.path.dirname(os.path.realpath(sys.argv[0]))