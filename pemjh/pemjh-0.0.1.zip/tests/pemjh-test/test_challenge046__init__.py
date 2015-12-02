""" Tests for challenge046 """
from pemjh.challenge046 import challenge046
import pytest


@pytest.mark.regression
def test_challenge046():
    """ Regression testing challenge046 """
    assert challenge046() == 5777
