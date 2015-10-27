# Copyright (c) 2015. Mount Sinai School of Medicine
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function, division, absolute_import

from six.moves import intern
from typechecks import is_string, is_integer

# Manually memoizing here, since our simple common.memoize function has
# noticable overhead in this instance.
NORMALIZE_CHROMOSOME_CACHE = {}

def normalize_chromosome(c):
    try:
        return NORMALIZE_CHROMOSOME_CACHE[c]
    except KeyError:
        pass

    if not (is_string(c) or is_integer(c)):
        raise TypeError("Chromosome cannot be '%s' : %s" % (c, type(c)))

    result = str(c)
    if result == "0":
        raise ValueError("Chromosome name cannot be 0")
    elif result == "":
        raise ValueError("Chromosome name cannot be empty")

    # only strip off lowercase chr since some of the non-chromosomal
    # contigs start with "CHR"
    if result.startswith("chr"):
        result = result[3:]

    # standardize mitochondrial genome to be "MT"
    if result == "M":
        result = "MT"
    else:
        # just in case someone is being lazy, capitalize "X" and "Y"
        result = result.upper()
    # interning strings since the chromosome names probably get constructed
    # or parsed millions of times, can save memory in tight situations
    # (such as parsing GTF files)
    result = intern(result)
    NORMALIZE_CHROMOSOME_CACHE[c] = result
    return result

def normalize_strand(strand):
    if strand == "+" or strand == "-":
        return strand
    elif strand == 1:
        return "+"
    elif strand == -1:
        return "-"

    raise ValueError("Invalid strand: %s" % (strand,))

class Locus(object):
    """
    Base class for any entity which can be localized at a range of positions
    on a particular strand of a chromosome/contig.
    """

    def __init__(
            self,
            contig,
            start,
            end,
            strand):
        """
        contig : str
            Chromosome or other sequence name in the reference assembly

        start : int
            Start position of locus on the contig

        end : int
            Inclusive end position on the contig

        strand : str
            Should we read the locus forwards ('+') or backwards ('-')?
        """

        self.contig = normalize_chromosome(contig)
        self.strand = normalize_strand(strand)

        start = int(start)
        end = int(end)

        if start == 0:
            raise ValueError("Expected start > 0 (using base 1 coordinates)")
        elif end == 0:
            raise ValueError("Expected end > 0 (using base 1 coordinates)")

        if end < start:
            raise ValueError(
                "Expected start <= end, got start = %d, end = %d" % (
                    start, end))
        self.start = start
        self.end = end

    def __str__(self):
        return "Locus(contig=%s, start=%s, end=%s, strand=%s)" % (
            self.contig, self.start, self.end, self.strand)

    def __repr__(self):
        return str(self)

    def __len__(self):
        return self.end - self.start + 1

    def __eq__(self, other):
        return (
            isinstance(other, Locus) and
            self.contig == other.contig and
            self.start == other.start and
            self.end == other.end and
            self.strand == other.strand
        )

    def __hash__(self):
        return hash(str(self))

    @property
    def length(self):
        return self.end - self.start + 1

    def offset(self, position):
        """Offset of given position from stranded start of this locus.

        For example, if a Locus goes from 10..20 and is on the negative strand,
        then the offset of position 13 is 7, whereas if the Locus is on the
        positive strand, then the offset is 3.
        """
        if position > self.end or position < self.start:
            raise ValueError(
                "Position %d outside valid range %d..%d of %s" % (
                    position, self.start, self.end, self))
        elif self.on_forward_strand:
            return position - self.start
        else:
            return self.end - position

    def offset_range(self, start, end):
        """
        Database start/end entries are always ordered such that
        start < end. This makes computing a relative position (e.g. of a stop
        codon relative to its transcript) complicated since the "end"
        position of a backwards locus is actually earlir on the strand.
        This function correctly selects a start vs. end value depending
        on this locuses's strand and determines that position's offset from
        the earliest position in this locus.
        """
        assert start <= end, \
            "Locations should always have start < end, got start=%d, end=%d" % (
                start, end)

        if start < self.start or end > self.end:
            raise ValueError("Range (%d, %d) falls outside %s" % (
                start, end, self))

        if self.on_forward_strand:
            return (start - self.start, end - self.start)

        else:
            return (self.end - end, self.end - start)

    def on_contig(self, contig):
        return normalize_chromosome(contig) == self.contig

    def on_strand(self, strand):
        return normalize_strand(strand) == self.strand

    @property
    def on_forward_strand(self):
        return self.on_strand("+")

    @property
    def on_positive_strand(self):
        return self.on_forward_strand

    @property
    def on_backward_strand(self):
        return self.on_strand("-")

    @property
    def on_negative_strand(self):
        return self.on_backward_strand

    def can_overlap(self, contig, strand=None):
        """
        Is this locus on the same contig and (optionally) on the same strand?
        """
        return (
            self.on_contig(contig)
            and
            (strand is None or self.on_strand(strand)))

    def distance_to_interval(self, start, end):
        """
        Find the distance between intervals [start1, end1] and [start2, end2].
        If the intervals overlap then the distance is 0.
        """
        if self.start > end:
            # interval is before this exon
            return self.start - end
        elif self.end < start:
            # exon is before the interval
            return start - self.end
        else:
            return 0

    def distance_to_locus(self, other):
        if not self.can_overlap(other.contig, other.strand):
            # if two loci are on different contigs or strands,
            # can't compute a distance between them
            return float("inf")
        return self.distance_to_interval(other.start, other.end)

    def overlaps(self, contig, start, end, strand=None):
        """
        Does this locus overlap with a given range of positions?

        Since locus position ranges are inclusive, we should make sure
        that e.g. chr1:10-10 overlaps with chr1:10-10
        """
        return (
            self.can_overlap(contig, strand) and
            self.distance_to_interval(start, end) == 0)

    def overlaps_locus(self, other_locus):
        return self.overlaps(
            other_locus.contig,
            other_locus.start,
            other_locus.end,
            other_locus.strand)

    def contains(self, contig, start, end, strand=None):
        return (
            self.can_overlap(contig, strand) and
            start >= self.start and
            end <= self.end)

    def contains_locus(self, other_locus):
        return self.contains(
            other_locus.contig,
            other_locus.start,
            other_locus.end,
            other_locus.strand)
