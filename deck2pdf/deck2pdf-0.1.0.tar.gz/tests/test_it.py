import os
import shutil
import deck2pdf
from pytest import raises
from . import (
    current_dir,
    test_dir,
    skip_in_ci,
)


class TestForMain(object):
    def setUp(self):
        shutil.rmtree(os.path.join(current_dir, '.deck2pdf'), ignore_errors=True)

    def test_help(self):
        raises(SystemExit, deck2pdf.main, [])
        raises(SystemExit, deck2pdf.main, ['-h'])

    @skip_in_ci
    def test_files(self):
        test_slide_path = os.path.join(test_dir, 'testslide/_build/slides/index.html')
        deck2pdf.main([test_slide_path, ])
        assert os.path.exists(os.path.join(current_dir, '.deck2pdf'))
