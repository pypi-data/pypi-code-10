#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import sys
import os
import collections
from operator import itemgetter

ALIGNMENT_FILE = sys.argv[1]

# key: sequence lengths, val: number of times a sequence of key length appears
LENGTH_COUNTS = collections.defaultdict(lambda: 0) 

# Max number of digits of sequence length 
LENGTH_CHARS = 4

# The width of the terminal
TERMINAL_WIDTH = int(os.popen('stty size', 'r').read().split()[1])

# Count of the number of unique sequences.
COUNT_UNIQUE_SEQS = 0

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
	LENGTH_COUNTS[len(seq)] += int(count)

# Get min and max counts        
min_count = min(LENGTH_COUNTS.itervalues())
max_count = max(LENGTH_COUNTS.itervalues())
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
print "Number of reads: {}".format(sum(LENGTH_COUNTS.itervalues()))
print "MinCount: {}; MaxCount: {}".format(min_count, max_count)
print "Each ∎ represents a count of {}".format(square_size)

# Print histogram
for length in sorted(LENGTH_COUNTS):
    #     17 [ 19204]: ∎∎∎∎∎∎∎∎∎∎∎∎
    count = LENGTH_COUNTS[length] 
    bar_chars = count // square_size  
    print("{0:>{1}} [{2:>{3}}]: {4}".format(
            length, LENGTH_CHARS, count, max_count_chars, '∎' * bar_chars))

# Print suitable for input to Excel
print
print "Suitable for copy/paste into Excel:"
for length in sorted(LENGTH_COUNTS):
    count = LENGTH_COUNTS[length] 
    bar_chars = count // square_size  
    print "{}\t{}".format(length, count)
