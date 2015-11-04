import os
import fnmatch
import hashlib

def find_files_by_ending_in_directory(ending, directory):
    """Return paths to all files with `ending` in subfolders of `directory`"""
    file_list = [os.path.join(dirpath, f)
                 for dirpath, dirnames, files in os.walk(directory)
                 for f in fnmatch.filter(files, "*.{}".format(ending))]
    return file_list

def hash_file(path_to_file):
    """ Returns the MD5 Sum of a file"""
    BLOCKSIZE = 65536
    hasher = hashlib.md5()
    with open(path_to_file, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()
