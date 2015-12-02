""" Tests for challenge039 """
from pemjh.challenge039 import challenge039
import pytest


@pytest.mark.regression
def test_challenge039():
    """ Regression testing challenge039 """
    assert challenge039() == 840
