import glob
import os
import re

import requests
from Bio.SeqIO import SeqRecord
from Bio import SeqIO

from .utils import is_fasta


class PrimerDesigner:
    """Class for designing primers from FASTA files.

    It will send a FASTA alignment to `primers4clades`_ in order to design
    degenerate primers. Input data needed is an alignment in FASTA format
    containing at least 4 sequences.
    It is recommended that the beginning of each FASTA sequence description
    contains the taxon name between square brackets.

    Parameters:

        folder (str):                path of folder containing the FASTA file alignments
        taxon_for_codon_usage (str): optional taxon name that will be inserted in the
                                     description of FASTA sequences between square
                                     brackets so that can be used by primer4clades
                                     to infer the codon table to use
        tm (str):                    temperature
        min_amplength (str):         minimum amplicon length
        max_amplength (str):         maximum amplicon length
        gencode (str):               genetic code. See below for all available genetic
                                     codes
        clustype (str):              cluster distance metric: ``dna``, ``protein``.
        amptype (str):               substitution model used to estimate phylogenetic
                                     information
        email (str):                 your email address so that primer4clades can send
                                     you email with detailed results

    Example:

        >>> # The values shown are the default. Change them if needed.
        >>> from primer_designer import PrimerDesigner
        >>> pd = PrimerDesigner()
        >>> pd.folder = "alignments"   # folder containing the FASTA file alignments
        >>> pd.tm = "55"               # annealing temperature
        >>> pd.min_amplength = "250"   # minimum amplicon length
        >>> pd.max_amplength = "500"   # maximum amplicon length
        >>> pd.gencode = "universal"   # see below for all available genetic codes
        >>> pd.mode  = "primers"
        >>> pd.clustype = "dna"
        >>> pd.amptype = "dna_GTRG"    # substitution model used to estimate phylogenetic information
        >>> pd.email = "youremail@email.com"   # primer4clades will send you an email with very detailed results
        >>> pd.design_primers()
        >>>
        >>> # You can input a taxon name to include in the description of every
        >>> # FASTA sequence so that primer4clades can infer the correct codon
        >>> # table to apply to the analysis.
        >>> pd.taxon_for_codon_usage = "Bombyx mori"
        >>> pd.design_primers()

    The best primer pairs will be printed to your screen. Detailed results will
    be saved as HTML files in your alignments folder. But it is recommended if
    you also get the results by email. primers4clades_ will send you one email
    for each alignment.
    The genetic code table (variable ``gencode``) can be any of the following:

        * ``universal`` for standard
        * ``2`` for vertebrate mitochondrial
        * ``3`` for yeast mitochondrial
        * ``4`` for mold and protozoa mitochondrial
        * ``5`` for invertebrate mitochondrial
        * ``6`` for ciliate
        * ``9`` for echinoderm and flatworm
        * ``10`` for  euplotid nuclear
        * ``11`` for  bacterial and plastid
        * ``12`` for  alternative yeast nuclear
        * ``13`` for  ascidian mitochondrial
        * ``14`` for  flatworm mitochondrial
        * ``15`` for  Blepharisma nuclear
        * ``16`` for  Chlorophycean mitochondrial
        * ``21`` for  Trematode mitochondrial
        * ``22`` for  Scenedesmus obliquus mitochondrial
        * ``23`` for  Thraustochytrium mitochondrial

    The evolutionary substitution model can be any of the following (variable
    ``amptype``):

        * ``protein_WAGG``  for protein WAG+G
        * ``protein_JTTG``  for protein JTT+G
        * ``protein_Blosum62G``  for protein Blosum62+G
        * ``protein_VTG``  for protein VT+G
        * ``protein_DayhoffG``  for protein Dayhoff+G
        * ``protein_MtREVG``  for protein MtREV+G
        * ``dna_HKYG``  for dna HKY+G
        * ``dna_GTRG``  for dna GTR+G
        * ``dna_K80G``  for dna K80+G
        * ``dna_TrNG``  for dna TrN+G
        * ``dna_JC69G``  for dna JC69+G

    .. _primers4clades: http://floresta.eead.csic.es/primers4clades/#0
    """

    def __init__(self, folder=None, taxon_for_codon_usage=None, tm="55",
                 min_amplength="100", max_amplength="500", gencode="universal",
                 mode="primers", clustype="dna", amptype="dna_GTR", email=None):
        self.folder = folder
        self.taxon_for_codon_usage = taxon_for_codon_usage
        self.tm = tm
        self.min_amplength = min_amplength
        self.max_amplength = max_amplength
        self.gencode = gencode
        self.mode = mode
        self.clustype = clustype
        self.amptype = amptype
        self.email = email
        self.report = ""

    def design_primers(self):
        alns = self.get_alignments()

        if alns:
            self.call_primer4clades_for_primers(alns)

            # Write primers to alignment file
            with open("primers_report.txt", "a") as handle:
                handle.write(self.report)

            print("\nDone.\nAll primers have been saved in the file \"primers_report.txt\"")
            return self.report
        else:
            msg = "\nError! the folder {0} is empty.\n".format(self.folder)
            raise AttributeError(msg)

    def call_primer4clades_for_primers(self, alns):
        for aln in alns:
            if is_fasta(aln):

                if self.taxon_for_codon_usage:
                    aln = self.insert_taxon_in_new_fasta_file(aln)

                print("\nProcessing file \"{0}\"".format(aln))

                r = self.request_primers(aln)
                self.process_response(aln, r.text)

    def get_alignments(self):
        if os.path.exists(self.folder):
            all_files = os.path.join(self.folder, "*")
            alns = glob.glob(all_files)
        else:
            msg = "\nError! the folder {0} does not exist.\n".format(self.folder)
            raise AttributeError(msg)
        return alns

    def insert_taxon_in_new_fasta_file(self, aln):
        """primer4clades infers the codon usage table from the taxon names in the
        sequences.

        These names need to be enclosed by square brackets and be
        present in the description of the FASTA sequence. The position is not
        important. I will insert the names in the description in a new FASTA
        file.

        Returns:
            Filename of modified FASTA file that includes the name of the taxon.
        """
        new_seq_records = []
        for seq_record in SeqIO.parse(aln, 'fasta'):
            new_seq_record_id = "[{0}] {1}".format(self.taxon_for_codon_usage, seq_record.id)
            new_seq_record = SeqRecord(seq_record.seq, id=new_seq_record_id)
            new_seq_records.append(new_seq_record)

        base_filename = os.path.splitext(aln)
        new_filename = '{0}_modified{1}'.format(base_filename[0], base_filename[1])
        SeqIO.write(new_seq_records, new_filename, "fasta")
        return new_filename

    def process_response(self, aln, response_body):
        this_file = os.path.split(aln)[1]
        this_file = re.sub(".fas.*", "", this_file)

        msg = 'Writing detailed results as file "{0}.html"'.format(aln)
        print(msg)

        with open("{0}.html".format(aln), "w") as handle:
            handle.write(response_body)

        self.make_report_from_html_file(response_body, this_file)

    def make_report_from_html_file(self, response_body, this_file):
        """Processes the results from primer4clades (a html file).

        Makes a report based on the best possible primer pair (with highest
        quality and longest amplicon).
        """
        amplicon_tuples = self.get_amplicon_data_as_tuples(response_body)

        best_amplicon = self.choose_best_amplicon(amplicon_tuples)

        if best_amplicon is not None:
            self.report += """\n\n\
####################################################
# Alignment {0}
""".format(this_file)
            self.report += self.format_amplicon(best_amplicon)

    def get_amplicon_data_as_tuples(self, response_body):
        amplicons = re.findall("(## Amplicon.+) codon", response_body)
        primers_codehop = self.group_primers(re.findall("(\w+ codeh)_corr.+\n", response_body))
        primers_relaxed = self.group_primers(re.findall("(\w+ relax)_corr.+\n", response_body))
        primers_degen = self.group_primers(re.findall("(\w+ degen)_corr.+\n", response_body))
        primer_pair_qualities = re.findall("# primer pair.+= ([0-9]+)%\n", response_body)
        expected_pcr_product_lengths = re.findall("# expected PCR .+= ([0-9]+)\n", response_body)
        forward_temperatures = re.findall("(# fwd: minTm.+)\n", response_body)
        reverse_temperatures = re.findall("(# rev: minTm.+)\n", response_body)

        amplicon_tuples = zip(amplicons, primers_codehop, primers_relaxed,
                              primers_degen,
                              primer_pair_qualities,
                              expected_pcr_product_lengths,
                              forward_temperatures, reverse_temperatures)
        return amplicon_tuples

    def format_amplicon(self, best_amplicon):
        best_amplicon_formatted = ""
        for idx, value in enumerate(best_amplicon):
            if idx == 0:
                best_amplicon_formatted += "{0}".format(value).replace("##", "# Best")
            elif idx in [2, 3]:
                best_amplicon_formatted += "\n\n{0}".format(value)
            elif idx == 4:
                best_amplicon_formatted += "\n\n# primer pair quality = {0}%".format(
                    value)
            elif idx == 5:
                best_amplicon_formatted += "\n# expected PCR product length (nt) = {0}".format(
                    value)
            else:
                best_amplicon_formatted += "\n{0}".format(value)
        return best_amplicon_formatted

    def group_primers(self, my_list):
        """Group elements in list by certain number 'n'"""
        new_list = []
        n = 2
        for i in range(0, len(my_list), n):
            grouped_primers = my_list[i:i + n]
            forward_primer = grouped_primers[0].split(" ")
            reverse_primer = grouped_primers[1].split(" ")
            formatted_primers = ">F_{0}\n{1}".format(forward_primer[1], forward_primer[0])
            formatted_primers += "\n>R_{0}\n{1}".format(reverse_primer[1], reverse_primer[0])
            new_list.append(formatted_primers)
        return new_list

    def choose_best_amplicon(self, amplicon_tuples):
        """Iterates over amplicon tuples and returns the one with highest quality
        and amplicon length.
        """
        quality = 0
        amplicon_length = 0
        best_amplicon = None

        for amplicon in amplicon_tuples:
            if int(amplicon[4]) >= quality and int(amplicon[5]) >= amplicon_length:
                quality = int(amplicon[4])
                amplicon_length = int(amplicon[5])
                best_amplicon = amplicon

        return best_amplicon

    def request_primers(self, aln):
        url = "http://floresta.eead.csic.es/primers4clades/primers4clades.cgi"
        params = {
            'tm': self.tm,
            'min_amplength': self.min_amplength,
            'max_amplength': self.max_amplength,
            'mode': self.mode,
            'gencode': self.gencode,
            'clustype': self.clustype,
            'email': self.email,
        }
        files = {'sequencefile': open(aln, 'rb')}
        r = requests.post(url, files=files, data=params)
        return r
