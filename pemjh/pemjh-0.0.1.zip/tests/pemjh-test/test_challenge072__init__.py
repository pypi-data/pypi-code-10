""" Tests for challenge072 """
from pemjh.challenge072 import challenge072
import pytest


@pytest.mark.regression
def test_challenge072():
    """ Regression testing challenge072 """
    assert challenge072() == 303963552391L
