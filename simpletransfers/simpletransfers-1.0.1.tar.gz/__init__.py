"""
A set of classes that provide operations to
get files or put files to or from somewhere,
usually a network resource.

All these classes implement a get and put method,
for, well, getting and putting data.
"""
import os
import sys

class TransferException( Exception ):
	pass

from .local import local
from .ftp import ftp
from .sftp import sftp
from .mail import mail
from .http import http
from .wsgi import wsgi
from .zip import zipfile
from .soap import soap
