import random


def throwOneNum():
    # index = ''
    # In python 3, range() does what xrange() used to do and xrange() does not
    # exist
    # list(range(1, 10))
    # for x in range(1, 10):
        # index = index + ',' + '%d' % x
    # return index
   return random.choice(list(range(1, 10)))


print(throwOneNum())
