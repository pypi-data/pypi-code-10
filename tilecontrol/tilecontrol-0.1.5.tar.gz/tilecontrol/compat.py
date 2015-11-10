import sys


if sys.version_info > (3,):
    from urllib.request import urlopen as urlopen
else:
    from urllib import urlopen as urlopen
