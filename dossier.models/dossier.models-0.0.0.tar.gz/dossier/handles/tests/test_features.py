

import nltk
import pytest
from dossier.handles import features

@pytest.fixture(scope='session')
def nltk_data():
    nltk.download('all')

@pytest.fixture(scope='session')
def corpora(nltk_data):
    return features.initialize_corpora()

@pytest.mark.parametrize(
    'leetness',
    [
        'str1k3r',
        'l33t',
        'b0z0',
        'SiLeNt p0is0n',
    ]
)
def test_leet_speak(leetness, corpora):
    assert features.is_leet_speak(leetness, corpora)


@pytest.mark.parametrize(
    'unleetness',
    [
        'str1k3rboof',
        'unl33t',
        'a real bozopop',
    ]
)
def test_leet_speak_not(unleetness, corpora):
    assert not features.is_leet_speak(unleetness, corpora)
