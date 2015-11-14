from zerotest.response import Response

__author__ = 'Hari Jiang'


def test_response__str__():
    response = Response(200, {"just test": "hope pass"}, "happy test!")
    assert str(response) == """200
{'just test': 'hope pass'}
happy test!"""
