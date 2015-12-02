""" Challenge084 """
import random
from itertools import cycle


def roll_dice(rng):
    """ Throw two 4 sided dice.
    Return the sum and whether they are the same. """
    dice1 = rng.randint(1, 4)
    dice2 = rng.randint(1, 4)
    return dice1 + dice2, dice1 == dice2


def chance_deck():
    """ Setup the chance deck """
    cards = cycle([
        lambda _: 0,  # Advance to Go - Direct to 00
        lambda _: 10,  # Go to jail - Direct to 10
        lambda _: 11,  # Go to C1 - Direct to 11
        lambda _: 24,  # Go to E3 - Direct to 24
        lambda _: 39,  # Go to H2 - Direct to 39
        lambda _: 5,  # Go to R1 - Direct to 05
        lambda current: 17 if current == 7 else
        25 if current == 22 else 5,  # Go to next R - Direct to 05/15/25/35
        lambda current: 17 if current == 7 else
        25 if current == 22 else 5,  # Go to next R - Direct to 05/15/25/35
        lambda current: 28 if current == 22
        else 12,  # Go to next U - Direct to 12/28
        lambda current: current - 3,  # Go back 3 squares - -3
        lambda current: current,
        lambda current: current,
        lambda current: current,
        lambda current: current,
        lambda current: current,
        lambda current: current,
        lambda current: current])

    def chance_card_move(current):
        """ Return the space to move to """
        return cards.next()(current)

    return chance_card_move


def community_chest_deck():
    """ Setup the community chest deck """
    cards = cycle([
        lambda _: 0,  # Advance to Go - Direct to 00
        lambda _: 10,  # Go to jail - Direct to 10
        lambda current: current,
        lambda current: current,
        lambda current: current,
        lambda current: current,
        lambda current: current,
        lambda current: current,
        lambda current: current,
        lambda current: current,
        lambda current: current,
        lambda current: current,
        lambda current: current,
        lambda current: current,
        lambda current: current,
        lambda current: current])

    def community_chest_card_move(current):
        """ Return the space to move to """
        return cards.next()(current)

    return community_chest_card_move


def challenge084():
    """ challenge084 """
    current = 0

    chances = [[0, i] for i in xrange(40)]
    moves = 0

    double_count = 0

    rng = random.Random(42)

    chance_card_move = chance_deck()
    community_chest_card_move = community_chest_deck()

    # Play a move
    while moves < 100000:
        # Roll the dice and move
        roll, double = roll_dice(rng)
        current += roll
        if current > 39:
            current -= 40

        if double:
            double_count += 1
        else:
            double_count = 0

        # Check for special square
        if double_count == 3:
            # 3 doubles, jail
            current = 10
            # Reduce double count by 1 to allow for the next throw
            # to do the same
            double_count -= 1
        elif current == 30:
            current = 10
        elif current == 2 or current == 17 or current == 3:
            current = community_chest_card_move(current)
        elif current == 7 or current == 22 or current == 36:
            current = chance_card_move(current)

        # Move completed, record final position
        chances[current][0] += 1

        moves += 1

    top3 = sorted(chances)[-3:]

    return top3[2][1] * 10000 + top3[1][1] * 100 + top3[0][1]
