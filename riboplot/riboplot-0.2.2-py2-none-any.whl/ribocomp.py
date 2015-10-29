# -*- coding: utf-8 -*-
"""Out number of Ribo-Seq reads of all transcripts for two conditions"""
import os
import shutil
import zipfile
import logging
import argparse

import ribocore
import config

from pandas import DataFrame
from bokeh.charts import Bar
from bokeh.plotting import output_file, output_server, show, figure, cursession, Session
# Default is production
CONFIG = config.ProductionConfig()

log = logging.getLogger('riboplot')


class ErrorLogFormatter(logging.Formatter):
    """Custom error log format for the HTML file"""

    def format(self, record):
        return '<h2>RiboComp Error</h2><p>{}</p>'.format(record.msg)


def create_parser():
    """Argument parser. """
    parser = argparse.ArgumentParser(
        prog='ribocomp', description='Output number of Ribo-Seq reads of all transcripts for two different conditions')

    # required arguments
    required = parser.add_argument_group('required arguments')
    required.add_argument('-b1', '--ribo_file1', help='Ribo-Seq alignment file in BAM format', required=True)
    required.add_argument('-b2', '--ribo_file2', help='Ribo-Seq alignment file in BAM format', required=True)

    parser.add_argument('-m', '--html_file', help='Output file for results (HTML)', default='ribocount.html')
    parser.add_argument('-o', '--output_path', help='Files are saved in this directory', default='output')
    parser.add_argument('-d', '--debug', help='Flag. Produce debug output', action='store_true')

    return parser


def get_total_reads(bam_fileobj):
    """Return total reads for each transcript in the bam file."""
    total_reads = {}
    for transcript in bam_fileobj.references[:200]:
        total_reads[transcript] = bam_fileobj.count(transcript)
    return total_reads

def main(args):
    """Main program"""
    (ribo_file1, ribo_file2, output_path, html_file) = \
        (args.ribo_file1, args.ribo_file2, args.output_path, args.html_file)

    log.debug('Supplied arguments\n{}'.format(
        '\n'.join(['{:<20}: {}'.format(k, v) for k, v in vars(args).items()])))

    # error messages (simple format) are written to html file
    fh = logging.FileHandler(html_file)
    fh.setLevel(logging.ERROR)
    fh.setFormatter(ErrorLogFormatter('%(message)s'))
    log.addHandler(fh)

#    output_file('ribocomp.html')
    session = Session(root_url='http://localhost:5006')
    session.login('vimal', 'vimal')
    output_server('ribocomp2')
    with ribocore.open_pysam_file(ribo_file1, ftype='bam') as f, ribocore.open_pysam_file(ribo_file2, ftype='bam') as g:
        data = []
        for transcript in f.references[:2]:
            data.append({'transcript': transcript, 'reads': f.count(transcript), 'condition': 1})
            data.append({'transcript': transcript, 'reads': g.count(transcript), 'condition': 2})

    print data
    df = DataFrame.from_dict(data)
    #print df
    cursession().publish()
    p =  Bar(data, label='transcript', values='reads', group='condition', # Use the group feature
        title="RiboSeq read counts ", legend='top_left')
    show(p)



def run():
    """Run program"""
    parsed = create_parser()
    args = parsed.parse_args()
    main(args)


if __name__ == '__main__':
    run()



