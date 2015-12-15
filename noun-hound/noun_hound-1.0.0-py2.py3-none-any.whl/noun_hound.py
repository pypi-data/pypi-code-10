#! /bin/env python

'''
  Copyright 2015 David Lettier

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
'''

from __future__ import absolute_import
from __future__ import unicode_literals
from builtins import object

import os
import math
import pickle
import nltk
import logging

LOGGER = logging.getLogger('NounHound')
LOGGER.setLevel(logging.INFO)
FORMATTER = logging.Formatter(
    '%(levelname)s %(name)s %(asctime)s => %(message)s'
)
STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setFormatter(FORMATTER)
STREAM_HANDLER.setLevel(logging.INFO)
LOGGER.addHandler(STREAM_HANDLER)

MODULE_PATH = os.path.abspath(os.path.dirname(__file__))


class NounHound(object):
  '''
    Extracts nouns and noun phrases from given text.
  '''

  def __init__(self):
    '''
      >>> n = NounHound()
      >>> n.noun_phrase_regex
      u'NP: {<(DT|JJ.*?|CD.*?|VB.*?)>*?<(N.*?)>+}'
      >>> n.tagset
      >>> n.load_called
      False
    '''

    self.noun_phrase_regex = r"NP: {<(DT|JJ.*?|CD.*?|VB.*?)>*?<(N.*?)>+}"
    self.noun_phrase_parser = None
    self.perceptron_tagger = None
    self.tagset = None
    self.load_called = False

  def load(self):
    '''
      >>> n = NounHound()
      >>> n.load() # doctest: +ELLIPSIS
      [nltk_data] Downloading package averaged_perceptron_tagger to
      [nltk_data]     ...
      [nltk_data]   Package averaged_perceptron_tagger is already up-to-
      [nltk_data]       date!
      [nltk_data] Downloading package brown to ...
      [nltk_data]   Package brown is already up-to-date!
      >>> n.perceptron_tagger # doctest: +ELLIPSIS
      <nltk.tag.perceptron.PerceptronTagger object at 0x...>
      >>> n.load_called
      True
    '''

    if not self.load_called:
      self.noun_phrase_parser = nltk.RegexpParser(
          self.noun_phrase_regex
      )
      nltk.download('averaged_perceptron_tagger')
      nltk.download('brown')
      try:
        self.perceptron_tagger = pickle.load(
            open(
                os.path.normpath(
                    os.path.join(
                        MODULE_PATH, 'pickles', 'tagger.pkl'
                    )
                ),
                'rb'
            )
        )
      except Exception as error:
        LOGGER.error(error)
        self.perceptron_tagger = nltk.tag.perceptron.PerceptronTagger(
            load=False
        )
        self.perceptron_tagger.train(
            list(nltk.corpus.brown.tagged_sents())
        )
        pickle.dump(
            self.perceptron_tagger,
            open(
                os.path.normpath(
                    os.path.join(
                        MODULE_PATH, 'pickles', 'tagger.pkl'
                    )
                ),
                'wb'
            )
        )
      LOGGER.info('loaded.')
      self.load_called = True

  def process(self, text):
    '''
      >>> n = NounHound()
      >>> n.load() # doctest: +ELLIPSIS
      [...
      >>> result = n.process(
      ...     'This is an apple pie and that is a cherry pie. '
      ...     "Alice's desserts are great. Won't you try one?"
      ... )
      >>> result['noun_phrases']
      [u"Alice's desserts", u'cherry pie', u'apple pie']
      >>> result['nouns']
      [u"Alice's", u'desserts', u'cherry', u'apple', u'pie', u'pie']
    '''

    self.load()
    noun_phrases = []
    nouns = []
    for parsed_token_chunk in self._parse_tokenized_chunks(
        self._tokenize_chunks(
            self._make_chunks(
                self._clean_text(
                    self._text_to_unicode(
                        text
                    )
                )
            )
        )
    ):
      for node in parsed_token_chunk:
        if node.__class__.__name__ != 'Tree':
          continue
        if node.label() != 'NP':
          continue
        number_of_nouns = 0
        caps = 0
        length = 0
        tokens = []
        for parsed_token in node:
          token = parsed_token[0]
          token_noun = 0
          token_caps = 0
          token_length = len(token)
          if token_length <= 0:
            continue
          if parsed_token[1].startswith('N'):
            token_noun = 1
            token_caps = sum(
                [1 if x.isupper() else 0 for x in token]
            )
            if token_caps == token_length:
              token_caps = 1
            nouns.append(
                (
                    token_caps + math.log10(token_length),
                    token
                )
            )
          number_of_nouns += token_noun
          caps += token_caps
          length += token_length
          tokens.append(token)
        noun_phrases.append(
            (
                number_of_nouns + caps + math.log10(length),
                u' '.join(tokens)
            )
        )
    nouns.sort(reverse=True)
    noun_phrases.sort(reverse=True)
    return {
        u'noun_phrases': [x[1] for x in noun_phrases],
        u'nouns': [x[1] for x in nouns]
    }

  def _parse_tokenized_chunks(self, tokenized_chunks):
    '''
      >>> n = NounHound()
      >>> n.load() # doctest: +ELLIPSIS
      [...
      >>> n._parse_tokenized_chunks([['Apple']])
      [Tree('S', [Tree('NP', [(u'Apple', u'NN-HL')])])]
    '''

    return [
        self.noun_phrase_parser.parse(
            nltk.tag._pos_tag(
                tokenized_chunk,
                self.tagset,
                self.perceptron_tagger
            )
        ) for tokenized_chunk in tokenized_chunks
    ]

  def _tokenize_chunks(self, chunks):
    '''
      >>> n = NounHound()
      >>> n._tokenize_chunks(['Over here', 'over there.'])
      [[u'Over', u'here'], [u'over', u'there.']]
    '''

    return [
        self._tokenize_chunk(chunk) for chunk in chunks
    ]

  def _tokenize_chunk(self, chunk):
    '''
      >>> n = NounHound()
      >>> n._tokenize_chunk('This is a chunk.')
      [u'This', u'is', u'a', u'chunk.']
    '''

    return chunk.split()

  def _make_chunks(self, text):
    '''
      >>> n = NounHound()
      >>> n._make_chunks(
      ...   'Make this chunk, that chunk, and this @chunk #chunk.'
      ... )
      [u'Make this chunk', u'that chunk', u'this', u'chunk', u'chunk']
    '''

    chunk_stops = [
        u",",
        u'"',
        u'!',
        u'?',
        u' and ',
        u'(',
        u')',
        u'[',
        u']',
        u'{',
        u'}',
        u'--',
        u';',
        u':',
        u'`',
        u'#',
        u'@',
        u'\u2018',
        u'\u201C',
        u'\u201D',
        u'\u0022'
    ]
    for chunk_stop in chunk_stops:
      text = text.replace(chunk_stop, '.')
    chunks = text.split('.')
    chunks = map(lambda x: x.strip(), chunks)
    chunks = filter(lambda x: len(x) > 1, chunks)
    return chunks

  def _clean_text(self, text):
    '''
      >>> n = NounHound()
      >>> n._clean_text(u"Won\u2019t you   clean Bob's text?")
      u" Won't you clean Bob's text? "
    '''

    replacements = {
        u'\u2019': u"'",
    }
    for key, value in replacements.items():
      text = text.replace(key, value)
    text = u' ' + u' '.join(text.split()) + u' '
    return text

  def _text_to_unicode(self, text):
    b'''
      >>> n = NounHound()
      >>> n._text_to_unicode(None)
      u''
      >>> n._text_to_unicode(b'Test')
      u'Test'
      >>> n._text_to_unicode(b'\u2019')
      u'\\\\u2019'
      >>> n._text_to_unicode('\u2019')
      u'\u2019'
    '''

    if text is None:
      text = u''
    if isinstance(text, str):
      try:
        text = text.decode('utf8', 'ignore')
      except Exception:
        text = bytes(text, 'utf-8').decode('utf-8', 'ignore')
    return text
