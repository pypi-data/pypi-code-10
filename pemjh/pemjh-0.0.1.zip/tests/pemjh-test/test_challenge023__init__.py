""" Tests for challenge023 """
from pemjh.challenge023 import challenge023
import pytest


@pytest.mark.regression
def test_challenge023():
    """ Regression testing challenge023 """
    assert challenge023() == 4179871
