'''
Copyright (c) 2015 Skylable Ltd.
License: Apache 2.0, see LICENSE for more details.

'''
import logging

from importer import S3Importer
from stream import DownloadedFileStream, ChunkedStream
from exceptions import S3ImportException

__version__ = '0.2.1'

__all__ = [
    'S3Importer', 'DownloadedFileStream', 'ChunkedStream', 'S3ImportException'
]

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(logging.NullHandler())
