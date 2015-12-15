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