# import unittest
# from contracts.syntax import number, rvalue
# from contracts.library.comparison import comparison_expr, comparisons_expr
#
# class TestParsingNumbers(unittest.TestCase):
#
#     if False:
#         def test_parsing_numbers(self):
#             numbers = ['1.0', '-1.0', '+1', '-1', '+1.0', '1.0']
#
#             for n in numbers:
#                 print('Trying to check %r' % n)
#                 res = number.parseString(n, parseAll=True)
#                 print(n, res)
#
#             for n in numbers:
#                 print('Trying to check rvalue %r' % n)
#                 res = rvalue.parseString(n, parseAll=True)
#                 print(n, res)
#
#     def test_parsing_numbers_comparisons(self):
#
#         print(comparisons_expr)
#         numbers = ['1.0', '-1.0', '+1', '-1', '+1.0', '1.0', '1']
#         glyphs = ['=', '>=', '<=']
#         for n in numbers:
#             for g in glyphs:
#                 s = '%s%s' % (g, n)
#                 print('Trying to check comparison %r' % s)
#                 res = comparison_expr.parseString(n, parseAll=True)
#                 print(n, res)
