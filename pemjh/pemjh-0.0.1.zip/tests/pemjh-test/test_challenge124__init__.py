""" Tests for challenge124 """
from pemjh.challenge124 import challenge124
import pytest


@pytest.mark.regression
def test_challenge124():
    """ Regression testing challenge124 """
    assert challenge124() == 21417
