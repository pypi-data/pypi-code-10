# -*- coding: utf-8 -*-

from multiprocessing import Pool
from functools import partial
import urllib.request
import shutil
import os


def _download(url, directory):
    file_name = os.path.join(directory, url.split('/')[-1])
    urlopen = urllib.request.urlopen

    with urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)


def pyrallelize(url_list, directory=''):
    if isinstance(url_list, list):
        p = Pool(len(url_list))
        p.map(partial(_download, directory=directory), url_list)
    elif isinstance(url_list, str):
        _download(url_list, directory)
    else:
        raise TypeError()
