""" Challenge054 """
from os.path import dirname, abspath


def get_duplicate_counts(hand):
    """
    >>> get_duplicate_counts(["10H", "10C", "09H", "13S", "03D"])
    {'10': 2}
    >>> dup = get_duplicate_counts(["10H", "09C", "08D", "08C", "09D"])
    >>> dup == {'09': 2, '08': 2}
    True
    >>> get_duplicate_counts(["10H", "10C", "10D", "10S", "10?"])
    {'10': 5}
    """
    value_counts = dict()
    for val in [c[:2] for c in hand]:
        if val in value_counts:
            value_counts[val] += 1
        else:
            value_counts[val] = 1

    return dict([[val, count] for val, count in value_counts.iteritems()
                 if count > 1])


def is_straight(hand):
    """
    >>> is_straight(["02C", "03D", "04D", "05H", "06C"])
    True
    >>> is_straight(["02C", "03D", "04D", "06C", "07H"])
    False
    >>> is_straight(["10D", "11C", "12D", "13H", "14D"])
    True
    """
    # Get just the numbers
    nums = list([int(c[:2]) for c in hand])

    # Assume no duplicates, first and last should be 4 apart
    return nums[4] - nums[0] == 4


def is_flush(hand):
    """
    >>> is_flush(["01H", "02H", "05H", "09H", "10H"])
    True
    >>> is_flush(["01H", "02H", "05H", "09H", "10D"])
    False
    """
    return len(set([c[2:] for c in hand])) == 1


def score_duplicates(duplicates):
    """ Score a hand with a single set of duplicates.
    The score is:
    2 for a pair,
    4 for 3 of a kind
    8 for 4 of a kind.
    Add on 0.01 * the value of the duplicate to discriminate face values. """
    count = duplicates.values()[0]
    if count == 2:
        # One Pair
        return 2.0 + int(duplicates.keys()[0]) * 0.01
    elif count == 3:
        # Three of a Kind
        return 4.0 + int(duplicates.keys()[0]) * 0.01
    else:
        # Four of a Kind
        return 8.0 + int(duplicates.keys()[0]) * 0.01


def score_2_duplicates(duplicates):
    """ Score a hand with multiple duplicates (2 of a kind/full house """
    duplicate_count_1 = duplicates.values()[0]
    duplicate_count_2 = duplicates.values()[1]
    duplicate_value_1 = int(duplicates.keys()[0])
    duplicate_value_2 = int(duplicates.keys()[1])
    if duplicate_count_1 == 2 and duplicate_count_2 == 2:
        # Two Pair
        if duplicate_value_1 > duplicate_value_2:
            return 3.0 + \
                duplicate_value_1 * 0.01 + \
                duplicate_value_2 * 0.0001
        else:
            return 3.0 + \
                duplicate_value_2 * 0.01 + \
                duplicate_value_1 * 0.0001
    else:
        # Full House
        if duplicate_count_1 > duplicate_count_2:
            return 7.0 + \
                duplicate_value_1 * 0.01 + \
                duplicate_value_2 * 0.0001
        else:
            return 7.0 + \
                duplicate_value_2 * 0.01 + \
                duplicate_value_1 * 0.0001


def score_hand(hand):
    """
    1 High Card
    2 One Pair
    3 Two Pair
    4 Three of a Kind
    5 Straight
    6 Flush
    7 Full House
    8 Four of a Kind
    9 Straight Flush
    10 Royal Flush
    """

    # Check for any duplicate face values, since this rules in
    duplicates = get_duplicate_counts(hand)
    if len(duplicates) == 1:
        return score_duplicates(duplicates)
    elif len(duplicates) == 2:
        return score_2_duplicates(duplicates)
    else:
        # Check for straight
        if is_straight(hand):
            if is_flush(hand):
                # Straight Flush
                # Royal Flush
                return 9.0 + \
                    int(hand[4][:2]) * 0.01
            else:
                # Straight
                return 5.0 + \
                    int(hand[4][:2]) * 0.01
        else:
            if is_flush(hand):
                # Flush
                return 6.0 + \
                    int(hand[4][:2]) * 0.01
            else:
                # High Card
                return 1.0 + \
                    int(hand[4][:2]) * 0.01


def compare_hands(hand_one, hand_two):
    """ Compare two hands.
    Return:
    0 if the hands are equal,
    -1 if the first hand beats the second
    1 if the second hand beats the first
    """
    # Sort both hands
    hand_one.sort()
    hand_two.sort()
    hand_one_score, hand_two_score = score_hand(hand_one), score_hand(hand_two)
    if hand_one_score > hand_two_score:
        return -1
    elif hand_one_score < hand_two_score:
        return 1
    else:
        for card_value_1, card_value_2 in [[card_value_1[:2], card_value_2[:2]]
                                           for card_value_1, card_value_2
                                           in zip(reversed(hand_one),
                                                  reversed(hand_two))]:
            if card_value_1 > card_value_2:
                return -1
            elif card_value_1 < card_value_2:
                return 1
        return 0


def challenge054():
    """ challenge054 """
    face_convert = {"2": "02", "3": "03", "4": "04", "5": "05",
                    "6": "06", "7": "07", "8": "08", "9": "09", "T": "10",
                    "J": "11", "Q": "12", "K": "13", "A": "14"}
    number_hand_one_wins = 0
    with open("%s/poker.txt" % dirname(abspath(__file__))) as hand_file:
        for line in hand_file:
            cards = list(face_convert[c[0]] + c[1]
                         for c in line.strip().split(" "))

            handone = cards[:5]
            handtwo = cards[5:]

            # Compare hands
            compare = compare_hands(handone, handtwo)
            if compare == -1:
                number_hand_one_wins += 1

    return number_hand_one_wins
