""" Tests for challenge166 """
from pemjh.challenge166 import challenge166
import pytest


@pytest.mark.regression
def test_challenge166():
    """ Regression testing challenge166 """
    assert challenge166() == 7130034
