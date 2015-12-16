import re

def chain_sub_regexes(phrase, *regex_sub_pairs):
    for regex, substitution in regex_sub_pairs:
        if isinstance(regex, basestring):
            regex = re.compile(regex)
        phrase = regex.sub(substitution, phrase)
    return phrase
