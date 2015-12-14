import unittest
import pysentosa.volatility as vo



def fun(x):
  v = vo.Volatility()
  return x + 1


class MyTest2(unittest.TestCase):
    def test(self):
        self.assertEqual(fun(3), 4)

if __name__ == '__main__':
    unittest.main()
