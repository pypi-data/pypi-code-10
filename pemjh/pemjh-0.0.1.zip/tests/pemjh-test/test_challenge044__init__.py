""" Tests for challenge044 """
from pemjh.challenge044 import challenge044
import pytest


@pytest.mark.regression
def test_challenge044():
    """ Regression testing challenge044 """
    assert challenge044() == 5482660
