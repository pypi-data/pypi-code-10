""" Challenge075 """
from pemjh.utilities.numbers import getPrimitiveTriples


def challenge075():
    """ challenge075 """
    limit = 2000000
    wire_lengths = dict()

    # Generate triples lower than target
    for total, length_a, length_b, length_c in \
        [(length_a + length_b + length_c,
          length_a, length_b, length_c)
         for length_a, length_b, length_c in getPrimitiveTriples(limit)]:

        # How many times does total go into limit?
        div = limit // total

        for k in xrange(1, div + 1):
            trip = k * total

            if trip in wire_lengths:
                wire_lengths[trip].add(tuple([k * length_a,
                                              k * length_b,
                                              k * length_c]))
            else:
                wire_lengths[trip] = set([tuple([k * length_a,
                                                 k * length_b,
                                                 k * length_c])])

    wire_lengths = [i[0] for i in wire_lengths.iteritems() if len(i[1]) == 1]
    return len(wire_lengths)
