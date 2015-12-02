""" Tests for challenge100 """
from pemjh.challenge100 import challenge100
import pytest


@pytest.mark.regression
def test_challenge100():
    """ Regression testing challenge100 """
    assert challenge100() == 756872327473L
