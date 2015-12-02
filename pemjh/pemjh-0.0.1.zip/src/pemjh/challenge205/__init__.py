""" Challenge205 """


def product(*args):
    if not args:
        return iter(((),))
    return (items + (item,)
            for items in product(*args[:-1]) for item in args[-1])


def diceRolls(nDice, nSides):
    rolls = [range(1, nSides + 1)] * nDice
    totals = [sum(n) for n in product(*rolls)]
    nRolls = len(totals)
    chances = [0] * (nDice * nSides + 1)
    for n in totals:
        chances[n] += 1
    return chances, nRolls


def challenge205():
    """ challenge205 """
    pete, nPete = diceRolls(9, 4)
    colin, nColin = diceRolls(6, 6)
    colin = dict([[n, freq] for n, freq in enumerate(colin) if freq > 0])
    peteWin = list()
    totalRolls = nPete * nColin
    for n, f in colin.iteritems():
        # Get the number of rolls pete would win on
        nWins = sum(pete[n + 1:])
        peteWin.append(f * nWins)

    return round(float(sum(peteWin)) / totalRolls, 7)
