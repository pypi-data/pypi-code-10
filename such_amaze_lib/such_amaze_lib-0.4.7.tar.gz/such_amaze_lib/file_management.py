"""
    This module contain useful function file managing or logging
"""
import shutil
import pickle

import os
import re


def iterate_file_name(file_name):
    """
        Check if file_name is already a file and then return a new file_name, windows style.

        :Example:
            >>> for i in range(0, 10):
            ...     f = open(iterate_file_name('salut.txt'), 'w')
            ...     f.close()
            ... 

    :param file_name: the file_name to scan
    :return: str
    """
    file_without_ext, ext = os.path.splitext(file_name)
    if os.path.isfile(file_name):
        n = 2
        while os.path.isfile('{} ({}){}'.format(file_without_ext, n, ext)):
            n += 1
        return '{} ({}){}'.format(file_without_ext, n, ext)
    return file_name


def load_results_pickle(pickle_file_path):
    """
        Load object from file

        >>> my_list = [e for e in range(0, 100) if e % 7 == 0]
        >>> with open('test_pickle.p', "wb") as f:
        ...     pickle.dump(my_list, f)
        ... 
        >>> print load_results_pickle('test_pickle.p')
        [0, 7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84, 91, 98]

    :param pickle_file_path: pickle file path
    :return: object
    """
    with open(pickle_file_path, "rb") as f:
        return pickle.load(f)


def purge(directory, pattern):
    """
        Delete recursively all the files that match the current pattern

            :Example:
                >>> # will delete all *.foobar file in the current working directory
                >>> file_name = 'foo.foobar'
                >>> with open(file_name, 'w') as f:
                ...     f.write('foo bar')
                ...     f.close()
                ... 
                >>> os.path.exists(file_name)
                True
                >>> purge('.', '.*\.foobar')
                >>> os.path.exists(file_name)
                False


    :param directory: the directory to scan
    :param pattern: the matching pattern
    """

    for root, _, files in os.walk(directory):
        for f in os.listdir(root):
            if re.search(pattern, f):
                os.remove(os.path.join(root, f))


def rm_tree(directory):
    """
        remove recursively directory if exists

    :param directory: directory name to erase
    """
    if os.path.exists(directory):
        shutil.rmtree(directory)


def create_dirs_if_not_exists(the_path):
    """
     Create all the directory tree of not exists

    :param the_path: the path to create if not exists
    """
    if not os.path.exists(os.path.abspath(the_path)):
        os.makedirs(the_path)
