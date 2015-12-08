"""
Testing of the fief module.

"""

from fief import filter_effective_parameters as fief


EFFECTIVE_PARAMETERS = {
    'a': 2,
    'b': 3,
    'c': 4,
}


@fief
def funcA(a, b):
    return a + b


# Here is dragons
#  Expected error:
#      TypeError: funcA() got an unexpected keyword argument 'c'
#  But the fief decorator removes the problem:
assert funcA(**EFFECTIVE_PARAMETERS) == 5
