""" Challenge080 """
from math import sqrt


def build_root(square_num, num):
    """ Get decimal total to 100 digits """

    def get_next_num(previous):
        """ Get next number """
        for j in xrange(10):
            if (previous + j) * j > current:
                return j - 1
        return 9

    # Convert the number to a string
    current = square_num
    prev_num = 0
    answer = list()

    for _ in xrange(num):
        # Loop through 0 - 9 until goes over current
        next_num = get_next_num(prev_num)
        answer.append(next_num)

        current -= (prev_num + next_num) * next_num
        current *= 100

        prev_num = (prev_num + (next_num * 2)) * 10

    return answer


def challenge080():
    """ challenge080 """
    total = 0
    for i in xrange(1, 100):
        if sqrt(i) != int(sqrt(i)):
            total += sum(build_root(i, 100))

    return total
