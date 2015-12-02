""" Tests for challenge115 """
from pemjh.challenge115 import challenge115
import pytest


@pytest.mark.regression
def test_challenge115():
    """ Regression testing challenge115 """
    assert challenge115() == 168
