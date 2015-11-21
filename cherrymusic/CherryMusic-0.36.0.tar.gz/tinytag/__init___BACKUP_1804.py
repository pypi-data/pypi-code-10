#!/usr/bin/python
# -*- coding: utf-8 -*-
from .tinytag import TinyTag, ID3, Ogg, Wave, Flac


<<<<<<< HEAD
__version__ = '0.10.1'
=======
__version__ = '0.8.0'
>>>>>>> origin/id3-images

if __name__ == '__main__':
    print(TinyTag.get(sys.argv[1]))