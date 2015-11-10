import unittest
from contracts.main import fail

class TestNumpyComparisons(unittest.TestCase):

    def test_parsing_numbers(self):
        import contracts
        try:
            import numpy
        except:
            return

        v = numpy.arange(1)[0]  # type(v) == numpy.int64 etc...
        c = '=0'

        contracts.check(c, v)


        fail('=1', v)

