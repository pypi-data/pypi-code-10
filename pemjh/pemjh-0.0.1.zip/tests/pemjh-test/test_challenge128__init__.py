""" Tests for challenge128 """
from pemjh.challenge128 import challenge128
import pytest


@pytest.mark.regression
def test_challenge128():
    """ Regression testing challenge128 """
    assert challenge128() == 14516824220L
