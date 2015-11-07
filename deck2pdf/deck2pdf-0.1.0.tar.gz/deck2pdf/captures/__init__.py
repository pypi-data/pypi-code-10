# -*- coding:utf8 -*-
"""Capturing engins
"""
import os
import logging
import importlib
import shutil
from .. import errors


Logger = logging.getLogger('deck2pdf.captures')

TEMP_CAPTURE_DIR = '.deck2pdf'


def find_engine(name):
    try:
        import_ = importlib.import_module('.{}'.format(name), 'deck2pdf.captures')
        return import_.CaptureEngine
    except ImportError:
        return None


def resolve_path(path):
    if path.startswith('http://'):
        return path
    elif path.startswith('https://'):
        return path
    realpath = os.path.abspath(path)
    if not os.path.exists(realpath):
        raise errors.ResourceNotFound()
    return 'file://{}'.format(realpath)


class CaptureEngine(object):
    """Slide capturing engine (abstract)
    """
    def __init__(self, url):
        self._url = resolve_path(url)
        self._slide_captures = []

    @property
    def url(self):
        return self._url

    @property
    def save_dir(self):
        current_dir = os.path.abspath(os.getcwd())
        return os.path.join(current_dir, TEMP_CAPTURE_DIR)

    def capture_all(self):
        """Capture all pages of slide
        """
        raise NotImplementedError()

    def capture_page(self, page_options):
        """Capture per page of slide, and save as pdf
        """
        raise NotImplementedError()

    def start(self):
        shutil.rmtree(self.save_dir, True)
        os.makedirs(self.save_dir)

    def end(self):
        raise NotImplementedError()
