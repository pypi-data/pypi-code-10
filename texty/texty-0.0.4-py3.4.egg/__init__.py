import os
import re


def guess_syllables(token_str, estimate_risk=False):
    """ Uses hardcoded rules to guess syllables for English words, optionally
        indicates estimated risk of error. The rules are not perfect,
        but testing shows decent results. Postcorrection is advised.
    """
    token_str = token_str.lower()
    vow_cluster_re = re.compile(r"[aeiou]+")
    # ending in consonant + e
    final_e_re = re.compile(r"[^aeiou]e+\b")
    # ending in two consonants + y or just consontant + y for 2-letter words
    final_2cons_y_re = re.compile(r"([^aeiou]{2,}y\b)|(\b[^aeiou]+y\b)")
    guess = 0
    risk = 0
    vowels = vow_cluster_re.findall(token_str)
    # Initially add one syllable per vowel cluster
    for vc in vowels:
        guess += 1
        if vc in ("ue", "ei"):  # see below
            risk += 1
    # --- START of token_str --- #
    # starts with "rei" => assume "re-i" and remove syllable (fails for reign etc.)
    if token_str.startswith("rei"):
        guess += 1
    # --- END of token_str --- #
    # ends with 2+ consonants & y => treat y as vowel and add syllable
    final_2cons_y = final_2cons_y_re.search(token_str)
    if final_2cons_y:
        guess += 1
        risk += 1
    else:
        final_e = final_e_re.search(token_str)
        # if only one vowel, then treat final e as syllable indicator
        if final_e and guess > 1:
            # ends with e but not "ee" => assume "e" is not indicator of syllable (so remove one)
            guess -= 1
    # Is it worthwhile / possible to make a good rule for ue  (e.g. "true") vs u-e (e.g. "fluent")?
    if estimate_risk:
        return guess, risk
    else:
        return guess


def concatenate_textfiles(source, out_path, ext=".txt", recursive=False, seperator="\n",
                          return_text=False, verbose=False):
    text = ""
    if type(source) == list:
        for p in source:
            try:
                with open(p, "r") as handler:
                    if verbose:
                        print("Adding text from", p)
                    text = "{}{}{}".format(text, seperator, handler.read())
            except IOError:
                pass
    elif type(source) == str:
        if not source:
            source = os.getcwd()  # for empty string, use current working directory
        paths = []
        if recursive:
            for root, dirnames, filenames in os.walk(source):
                for f in filenames:
                    if ext:
                        if f.endswith(ext):
                            p = os.path.join(root, f)
                            paths.append(p)
                    else:
                        p = os.path.join(root, f)
                        paths.append(p)
        else:
            if ext:
                for p in os.listdir(source):
                    if p.endswith(ext):
                        paths.append(p)
            else:
                paths = os.listdir(source)
        for p in paths:
            try:
                with open(p, "r") as handler:
                    if verbose:
                        print("Adding text from", p)
                    text = "{}{}{}".format(text, seperator, handler.read())
            except IOError:
                pass
    with open(out_path, "w") as handler:
        handler.write(text)
        if verbose:
            print("The concatenated text was saved as", out_path)
    if return_text:
        return text


def tokenize_str(s, word_chars="0-9A-Za-z\-'_"):
    not_word_chars = "[^{0}]+".format(word_chars)
    tokens = re.split(r'{0}'.format(not_word_chars), s, flags=re.UNICODE)
    tokens = [_t for _t in tokens if _t]
    return tokens


class SpacyHelper():

    def __init__(self, tag=True, parse=True, ner=True):
        try:
            import spacy.en
        except ImportError as e:
            print("Please make sure that spaCy is installed ('pip3 install spacy') and that English data is downloaded ('python3 -m spacy.en.download')")
            print("To download the English data, use: 'python3 -m spacy.en.download'")
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
    sh = SpacyHelper(parse=False)
    test_str = "Ankh-Morpork! Pearl of cities! This is not a completely accurate description, " \
               "of course — it was not round and shiny — but even its worst enemies would agree "\
               "that if you had to liken Ankh-Morpork to anything, then it might as well be a "\
               "piece of rubbish covered with the diseased secretions of a dying mollusc."
    v_str = sh.tag_string(test_str)
    print(v_str)
    tokens = tokenize_str(test_str)
    for tok in tokens:
        syl = guess_syllables(tok)
        print(tok, syl)

if __name__ == "__main__":
    demo()