""" Challenge121 """
from pemjh.utilities.numbers import fact


def winChance(probs, losses):  # probs are always 1 in...
    if losses == 0:
        return 1

    chances = 0
    # Could it be a win?
    if len(probs) > losses:
        # Win, recur
        chances += winChance(probs[1:], losses)

    # Loss
    chances += (probs[0] - 1) * winChance(probs[1:], losses - 1)

    return chances


def play(turns):
    den = fact(turns + 1)
    lossesAllowed = turns // 2
    if not (turns & 1):
        lossesAllowed -= 1

    chances = 0
    probs = range(2, turns + 2)
    for losses in xrange(lossesAllowed + 1):
        wc = winChance(probs, losses)
        chances += wc

    prize = den // chances
    return prize


def challenge121():
    """ challenge121 """
    return play(15)
