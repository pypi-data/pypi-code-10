#!/usr/bin/env python
import sys
import os
import logging
import argparse


__version__ = '0.1.1'


Logger = logging.getLogger('deck2pdf')

TEMP_CAPTURE_DIR = '.deck2pdf'


def count_slide_from_dom(body):
    # FIXME: Too bad know-how
    import re
    return len(re.split('<\/slide>', body)) - 1


parser = argparse.ArgumentParser()
parser.add_argument('path', help='Slide endpoint file path', type=str)
parser.add_argument('-c', '--capture', help='Slide capture engine name', type=str, default='ghostpy')
parser.add_argument('-o', '--output', help='Output slide file path', type=str, default='./slide.pdf')


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parser.parse_args(argv)
    args.path = os.path.abspath(args.path)

    root_dir = os.getcwd()
    cache_dir = os.path.join(root_dir, TEMP_CAPTURE_DIR)
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    elif not os.path.isdir(cache_dir):
        # TODO: Modify custom exception?
        raise Exception('{} is not directory.'.format(cache_dir))

    # Capture
    from deck2pdf.captures import find_engine
    CaptureEngine = find_engine(args.capture)
    if CaptureEngine is None:
        raise Exception('Engine name "{}" is not found.'.format(args.capture))
    capture = CaptureEngine(args.path)
    capture.capture_all()

    # Merge
    pdf_path = os.path.abspath(args.output)

    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.pdfgen import canvas

    slide_size = landscape(A4)
    pdf = canvas.Canvas(pdf_path, pagesize=slide_size)
    idx = 0
    for slide in capture._slide_captures:
        pdf.drawImage(slide, 0, 0, slide_size[0], slide_size[1])
        pdf.showPage()
        idx += 1
    pdf.save()


if __name__ == '__main__':
    main()
