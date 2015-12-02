""" Tests for challenge164 """
from pemjh.challenge164 import challenge164
import pytest


@pytest.mark.regression
def test_challenge164():
    """ Regression testing challenge164 """
    assert challenge164() == 378158756814587L
