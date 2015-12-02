""" Tests for challenge056 """
from pemjh.challenge056 import challenge056
import pytest


@pytest.mark.regression
def test_challenge056():
    """ Regression testing challenge056 """
    assert challenge056() == 972
