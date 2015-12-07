# -*- coding: utf-8 -*-
"""It

Usage:
  prost_it SAMPLES_LIST_FILE

BLAH BLAH BLAH WRONG...
BLAH BLAH BLAH WRONG...
BLAH BLAH BLAH WRONG...
BLAH BLAH BLAH WRONG...

Arguments:
    SAMPLES_LIST_FILE   Usually named 'samples_list'

Options:
    -h, --help          Show this screen.
    -v, --version       Show the version.

"""

# Copyright (C) 2014, 2015  Peter Batzel and Jason Sydes
#
# This file is part of Prost!.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# You should have received a copy of the License with this program.
#
# Written by Jason Sydes and Peter Batzel.
# Advised by Thomas Desvignes.

###############
### Imports ###
###############

# Python 3 imports
from __future__ import absolute_import
from __future__ import division

# version
from prost._version import __version__

## Prost imports
###############import prost.constants

from prost.prost import (
    Samples,
    SamplesCounts)
from prost.common import (
    SlotPickleMixin,
    Progress)

## Other imports

from docopt import docopt
import sys
import os
import collections
from operator import itemgetter

#################
### Constants ###
#################

# Max number of digits of sequence length
LENGTH_CHARS = 4

# The width of the terminal
TERMINAL_WIDTH = int(os.popen('stty size', 'r').read().split()[1])

##################
### Singletons ###
##################

# Count of the number of unique sequences.
COUNT_UNIQUE_SEQS = 0

# key: sequence lengths, val: number of times a sequence of key length appears
LENGTHS_COUNTS = collections.defaultdict(lambda: 0)

# key: seq_length, val: (dict where key: seq, val: count per seq)
LENGTHS_SEQS_COUNTS = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))


#################
### Functions ###
#################


def read_sample_fastas(samples, lengths_seqs_counts, lengths_counts):
    """Read FASTA file of samples and create dictionary with associated
    (absolute only for now) counts per sample.

    Args:
        samples (Samples): The (populated) Samples singleton object.
    """

    print("Reading in all fasta files...")
    num_samples = len(samples)

    for sample_num, sample_name in enumerate(samples):
        num_entries = sum(1 for line in open(samples[sample_name], 'rU'))/2
        filename = os.path.basename(samples[sample_name])
        progress = Progress(
                'reading file{} ({})'.format(sample_num+1, filename),
                100000, num_entries)

        # populate absolute counts for this sample
        with open(samples[sample_name], 'rU') as in_fasta:
            for line in in_fasta:
                if line[0] == '>':
                    continue
                progress.progress()
                seq = line.strip()
                length = len(seq)

                # Track counts by length then seq
                lengths_seqs_counts[length][seq] += 1
                # Track counts just by length
                lengths_counts[length] += 1

        progress.done()


def command_line():
    """Entry point when calling this script from the command line.

    This function performs basic parsing of command line options, then hands
    off.

    By default, if no TSV files are passed in, all Prost! output files will be
    processed.

    """
    args = docopt(__doc__, version=__version__)

    # List of sample reads
    _samples = Samples()
    _samples._read_samples_filelist(args['SAMPLES_LIST_FILE'])

    read_sample_fastas(_samples, LENGTHS_SEQS_COUNTS, LENGTHS_COUNTS)
    exit()


    # in_prefix is always what the user tells us (out_prefix may not be, see
    # below)
    in_prefix = args['--in']

    # Build the list of tsv_filenames if not passed
    tsv_files = args['TSV_FILES']
    if not tsv_files:
        # Build the full list
        for suffix in prost.constants.OUTPUT_FILE_SUFFIXES:
            if in_prefix:
                tsv_files.append("{}_{}.tsv".format(in_prefix, suffix))
            else:
                tsv_files.append("{}.tsv".format(suffix))

    # Create one or many Workbooks
    if args['--many']:
        # out_prefix is exactly what the user tells us when running --many
        # mode.
        out_prefix = args['--out']

        # Create many workbooks, one for each TSV file.
        filenames = create_many(in_prefix, out_prefix, tsv_files)
        print "Created {}.".format(", ".join(filenames))
    else:
        # Do not allow blank out_prefix (as we would have nothing to name our
        # xlsx file)
        if args['--out']:
            out_prefix = args['--out']
        else:
            out_prefix = prost.constants.DEFAULT_OUTPUT_FILE_PREFIX

        # Create one big workbook
        filename = create_one(in_prefix, out_prefix, tsv_files)
        print "Created {}.".format(filename)



def orig():
    prev_seq = None
    with open(ALIGNMENT_FILE, 'r') as f:
        for line in f:
            if line[0] == '@':
                continue
            seq, count = line.split()[0].split('_')
            # Assumption: alignments for a given qname always appear together
            # (i.e. the SAM file is sorted by qname)
            # (BBMap produces SAM files sorted by qname.)
            if seq == prev_seq:
                continue
            prev_seq = seq
            COUNT_UNIQUE_SEQS += 1
        LENGTHS_COUNTS[len(seq)] += int(count)

    # Get min and max counts
    min_count = min(LENGTHS_COUNTS.itervalues())
    max_count = max(LENGTHS_COUNTS.itervalues())
    # Get the length in chars of the maximum count
    max_count_chars = len(str(max_count))

    # Num of chars into which we'll shove the squares.
    # 5 = " []: "
    # 3 = just a right margin
    max_bar_chars = TERMINAL_WIDTH - LENGTH_CHARS - max_count_chars - 5 - 3

    # How much each square represents
    square_size = max_count // max_bar_chars

    # Informational Header
    print "Number of unique sequences: {}".format(COUNT_UNIQUE_SEQS)
    print "Number of reads: {}".format(sum(LENGTHS_COUNTS.itervalues()))
    print "MinCount: {}; MaxCount: {}".format(min_count, max_count)
    print "Each ∎ represents a count of {}".format(square_size)

    # Print histogram
    for length in sorted(LENGTHS_COUNTS):
        #     17 [ 19204]: ∎∎∎∎∎∎∎∎∎∎∎∎
        count = LENGTHS_COUNTS[length]
        bar_chars = count // square_size
        print("{0:>{1}} [{2:>{3}}]: {4}".format(
                length, LENGTH_CHARS, count, max_count_chars, '∎' * bar_chars))

    # Print suitable for input to Excel
    print
    print "Suitable for copy/paste into Excel:"
    for length in sorted(LENGTHS_COUNTS):
        count = LENGTHS_COUNTS[length]
        bar_chars = count // square_size
        print "{}\t{}".format(length, count)


# vim: softtabstop=4:shiftwidth=4:expandtab
