""" Tests for challenge071 """
from pemjh.challenge071 import challenge071
import pytest


@pytest.mark.regression
def test_challenge071():
    """ Regression testing challenge071 """
    assert challenge071() == 428570
