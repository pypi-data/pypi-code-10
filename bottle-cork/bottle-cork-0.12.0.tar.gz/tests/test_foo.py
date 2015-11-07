
import pytest


@pytest.fixture(params=["merlinux.eu", "mail.python.org"])
def backend(request):
    print 'called with ', request.param
    return request.param

@pytest.fixture
def fixa(backend):
    return backend

@pytest.fixture
def fixb(backend):
    return backend + 'b'

def test_1(fixa):
    assert not fixa

def test_2(fixb):
    assert not fixb

