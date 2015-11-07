import os
import deck2pdf
from pytest import raises
from . import (
    current_dir,
)


def test_help():
    raises(SystemExit, deck2pdf.main, [])
    raises(SystemExit, deck2pdf.main, ['-h'])


def test_output_default():
    test_slide_path = os.path.join(__file__)
    deck2pdf.main([test_slide_path, '-c', 'stub'])
    assert os.path.exists(os.path.join(current_dir, '.deck2pdf'))
    assert os.path.exists(os.path.join(current_dir, 'slide.pdf'))


def test_output_file_by_name():
    output_path = os.path.join(current_dir, '.deck2pdf', 'test.output')
    test_slide_path = os.path.join(__file__)
    deck2pdf.main([test_slide_path, '-c', 'stub', '-o', output_path])
    assert os.path.exists(os.path.join(current_dir, '.deck2pdf'))
    assert os.path.exists(output_path)
