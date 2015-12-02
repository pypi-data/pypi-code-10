""" Tests for challenge065 """
from pemjh.challenge065 import challenge065
import pytest


@pytest.mark.regression
def test_challenge065():
    """ Regression testing challenge065 """
    assert challenge065() == 272
