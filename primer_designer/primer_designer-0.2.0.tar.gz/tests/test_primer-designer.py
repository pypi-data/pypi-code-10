import copy
import os
import unittest

from Bio import SeqIO
import responses

from primer_designer import PrimerDesigner


TEST_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Data')
ALIGNMENT = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Data', 'Ca2.fst')
RESPONSE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Data', 'response_Ca2.fst.html')


class PrimerDesignerTest(unittest.TestCase):
    def setUp(self):
        self.pd = PrimerDesigner(
            folder=TEST_FOLDER,
            tm="55",
            min_amplength="200",
            max_amplength="500",
            gencode="universal",
            mode="primers",
            clustype="protein",
            amptype="dna_GTRG",
            email="youremail@email.com",
        )
        self.tmp_folder= os.path.join(TEST_FOLDER, '..', 'tmp_folder')
        if not os.path.isdir(self.tmp_folder):
            os.mkdir(self.tmp_folder)
        self.maxDiff = None

    def tearDown(self):
        output_html_file = '{0}.html'.format(ALIGNMENT)
        if os.path.isfile(output_html_file):
            os.remove(output_html_file)

        if os.path.isfile(self.tmp_folder):
            os.remove(self.tmp_folder)

    def test_design_primers_from_empty_folder(self):
        pd = copy.copy(self.pd)
        pd.folder = self.tmp_folder
        self.assertRaises(AttributeError, pd.design_primers)

    def test_get_alignments(self):
        result = self.pd.get_alignments()
        self.assertTrue(len(result) > 0)

    def test_get_alignments_error(self):
        pd = copy.copy(self.pd)
        pd.folder = "fake_folder"
        self.assertRaises(AttributeError, pd.get_alignments)

    @responses.activate
    def test_request_primers(self):
        url = "http://floresta.eead.csic.es/primers4clades/primers4clades.cgi"
        with open(RESPONSE, 'r') as handle:
            response_html_body = handle.read()

        responses.add(responses.POST, url,
                      body=response_html_body,
                      status=200,
                      content_type='application/text',
                      )
        resp = self.pd.request_primers(ALIGNMENT)
        assert resp.content.decode('ascii') == response_html_body

    def test_report_from_html_response(self):
        expected = """\n\n\
####################################################
# Alignment Ca2.fst
# Best Amplicon 4
>F_codeh
GACCTGAAAGAAGAACTGggvaargghgc
>R_codeh
CCAGGTGTACCAGCGaadccraacca

>F_relax
GACCTGAAAGAAGAACTGggvaargghgc
>R_relax
CCAGGTGTACCAgcraadccraacca

>F_degen
gahytdaargaagaaytdggvaargghgc
>R_degen
ccnggdgtdccdgcraadccraacca

# primer pair quality = 80%
# expected PCR product length (nt) = 471
# fwd: minTm = 62.0 maxTm = 67.5
# rev: minTm = 65.5 maxTm = 68.8"""
        self.pd.process_response(ALIGNMENT, open(RESPONSE).read())
        self.assertEqual(expected, self.pd.report)

    def test_inserting_taxon_in_fasta_seq_descriptions(self):
        self.pd.taxon_for_codon_usage = 'Bombyx mori'
        modified_seq = self.pd.insert_taxon_in_new_fasta_file(os.path.join(TEST_FOLDER, 'Ca3.fst'))
        for seq_record in SeqIO.parse(modified_seq, 'fasta'):
            print(seq_record.description)
            self.assertTrue("Bombyx mori]" in seq_record.description)

        if os.path.isfile(modified_seq):
            os.remove(modified_seq)
