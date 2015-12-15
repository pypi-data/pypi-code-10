import os
import pandas as pd

class LabMTHelper():

    """ A simple class to score text with LabMT and pandas,
    based on the example provided by  Finn Årup Nielsen
    at http://neuro.imm.dtu.dk/wiki/LabMT  """

    def __init__(self, from_web=True, local_path=""):
        if from_web:
                source = ('http://www.plosone.org/article/'
                          'fetchSingleRepresentation.action?'
                          'uri=info:doi/10.1371/journal.pone.0026752.s001')
        else:
            if local_path:
                source = local_path
            else:
                source = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                      "journal.pone.0026752.s001.txt")
        try:
            labmt_csv = pd.read_csv(source, skiprows=2, sep='\t', index_col=0)
        except OSError as e:
            if from_web:
                print("\n\nThere were problems loading", source)
                print("If you have a local copy, you can set 'from_web=False' and specify " \
                      "'local_path'.\n\n")
            else:
                print("\n\nCould not open", source)
                print("If you don't have a local copy, you can set 'from_web=True' and load "\
                      "it from the original publication.\n\n")
            raise(e)


        else:
            self.avg_happiness = labmt_csv.happiness_average.mean()
            self.happiness = (labmt_csv.happiness_average - self.avg_happiness).to_dict()

    def score_tokens(self, tokens):
        score = sum([self.happiness.get(tok.lower(), 0.0)
                     for tok in tokens]) / len(tokens)
        return score

    def score_text(self, text):
        from texty.txt import tokenize_str
        tokens = tokenize_str(text)
        score = self.score_tokens(tokens)
        return score


class SpacyHelper():
    """ A wrapper for spaCy that provides some formatting and transformations."""

    def __init__(self, tag=True, parse=True, ner=True):
        try:
            import spacy.en
        except ImportError as e:
            print("\n\nPlease make sure that spaCy is installed ('pip3 install spacy') and that "\
                  "the English data is downloaded ('python3 -m spacy.en.download').\n\n")
            raise(e)
        else:
            self.nlp = spacy.en.English()
            self.tag = tag
            self.parse = parse
            self.ner = ner

    @staticmethod
    def format_in_line(tokens, delim="_"):
        s = ""
        for tok in tokens:
            s = "{} {}{}{}".format(s, tok, delim, tok.tag_)
        return s.strip()

    def format_vertical(self, tokens, delim="\t"):
        lines = []
        for tok in tokens:
            o = tok.orth_
            if self.tag:
                t = "{}{}".format(delim, tok.tag_)
            else:
                t = ""
            if self.ner:
                n = "{}{}".format(delim, tok.ent_type_)
            else:
                n = ""
            l = "{}{}".format(delim, tok.lemma_)
            lines.append("{}{}{}".format(o, t, n))
        line_str = "\n".join(lines)
        return line_str

    def tag_string(self, s, vertical=True, return_string=True):
        tokens = self.nlp(s, tag=self.tag, parse=self.parse, entity=self.ner)
        if return_string:
            if vertical:
                rs = self.format_vertical(tokens)
            else:
                rs = self.format_in_line(tokens)
            return rs
        else:
            return tokens

def demo():
    print("DEMO")
    test_str = "Ankh-Morpork! Pearl of cities! This is not a completely accurate description, " \
               "of course — it was not round and shiny — but even its worst enemies would agree "\
               "that if you had to liken Ankh-Morpork to anything, then it might as well be a "\
               "piece of rubbish covered with the diseased secretions of a dying mollusc.\n\n"
    print(test_str)
    print("\tSpacyHelper vertical part-of-speech and named entity tagging")
    sh = SpacyHelper(parse=False)
    v_str = sh.tag_string(test_str)
    print("\t\tv_str")
    print("\tLabMTHelper sentiment scoring")
    lh = LabMTHelper()
    score = lh.score_text(test_str)
    print("\t\t Text score:",score)

if __name__ == "__main__":
    demo()