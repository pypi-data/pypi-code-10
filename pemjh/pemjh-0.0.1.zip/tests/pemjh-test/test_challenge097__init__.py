""" Tests for challenge097 """
from pemjh.challenge097 import challenge097
import pytest


@pytest.mark.regression
def test_challenge097():
    """ Regression testing challenge097 """
    assert challenge097() == 8739992577L
