""" Tests for challenge225 """
from pemjh.challenge225 import challenge225
import pytest


@pytest.mark.regression
def test_challenge225():
    """ Regression testing challenge225 """
    assert challenge225() == 2009
