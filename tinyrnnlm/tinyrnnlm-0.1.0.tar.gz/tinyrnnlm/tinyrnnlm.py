#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict

import numpy

from .saveload import SaveLoad


def _sigmoid(x):
    """ safe sigmoid function
    :param numpy.ndarray x: input value (vector)
    :return: elementwise sigmoid
    :rtype: numpy.ndarray
    """
    clip_x = numpy.clip(x, -50., 50.)
    return 1. / (1. + numpy.exp(-clip_x))


def _softmax(x):
    """ safe softmax function
    :param numpy.ndarary x: input value (vector)
    :return: softmax(x)
    :rtype: numpy.ndarray
    """
    exp_x = numpy.exp(x - x.max())
    return exp_x / exp_x.sum()


def _read_header(fi):
    def set_header(header, fi, cast_type=None):
        line = fi.readline()
        if line == '\n' or cast_type is None:
            pass
        else:
            xs = line.rstrip().split(':')
            header[xs[0]] = cast_type(xs[1].strip())
    header = {}
    # version: 10
    # file format: 0
    #
    # training data file: amida-train.txt
    # validation data file: amida-valid.txt
    #
    # last probability of validation data: -111704.625972
    # number of finished iterations: 12
    # current position in training data: 0
    # current probability of training data: -111407.606233
    # save after processing # words: 0
    # # of training words: 752006
    set_header(header, fi, int)
    set_header(header, fi, int)
    set_header(header, fi)
    set_header(header, fi, str)
    set_header(header, fi, str)
    set_header(header, fi)
    set_header(header, fi, float)
    set_header(header, fi, int)
    set_header(header, fi, int)
    set_header(header, fi, float)
    set_header(header, fi, int)
    set_header(header, fi, int)
    # input layer size: 11656
    set_header(header, fi, int)
    # hidden layer size: 100
    set_header(header, fi, int)
    # compression layer size: 0
    # output layer size: 11606
    # direct connections: 0
    # direct order: 3
    # bptt: 9
    # bptt block: 10
    # vocabulary size: 11556
    set_header(header, fi, int)
    set_header(header, fi, int)
    set_header(header, fi, int)
    set_header(header, fi, int)
    set_header(header, fi, int)
    set_header(header, fi, int)
    set_header(header, fi, int)
    # class size: 50
    set_header(header, fi, int)
    # old classes: 0
    # independent sentences mode: 1
    # starting learning rate: 0.100000
    # current learning rate: 0.000781
    # learning rate decrease: 1
    #
    #
    set_header(header, fi, int)
    set_header(header, fi, int)
    set_header(header, fi, float)
    set_header(header, fi, float)
    set_header(header, fi, int)
    set_header(header, fi)
    set_header(header, fi)

    return header


def _read_hidden_layer_activation(fi):
    neu = []
    while True:
        line = fi.readline()
        if line == '\n' or line == '':
            break
        elif line == 'Hidden layer activation:\n':
            continue
        else:
            neu.append(float(line.rstrip()))
    return numpy.array(neu)


def _read_weight(fi):
    weight = []
    while True:
        line = fi.readline()
        if line == '\n' or line == '':
            break
        elif line == 'Weights 0->1:\n' or line == 'Weights 1->2:\n':
            continue
        else:
            weight.append(float(line.rstrip()))
    return numpy.array(weight)


def _read_direct_connections(fi):
    weight = []
    while True:
        line = fi.readline()
        if line == '\n' or line == '':
            break
        elif line == 'Direct connections:\n':
            continue
        else:
            weight.append(float(line.rstrip()))
    return numpy.array(weight)


def _minus_one():
    return -1


def _zero():
    return 0


def _minus_one_tuple():
    return (-1, -1)


class _TinyCRnnLMVocabList(object):

    def __init__(self):
        self._word2id = defaultdict(_minus_one)
        self._word2cn = defaultdict(_minus_one)
        self._word2class = defaultdict(_minus_one)
        self._class2size = defaultdict(_zero)
        self._class2range = defaultdict(_minus_one_tuple)

    @classmethod
    def read(cls, fi):
        def set_vocab(vocablist, fi):
            line = fi.readline()
            if line == 'Vocabulary:\n':
                return 0
            elif line == '\n':
                return 1
            else:
                xs = list(map(lambda x: x.strip(), line.rstrip().split('\t')))
                word_index = int(xs[0])
                cn = int(xs[1])
                word = xs[2]
                class_index = int(xs[3])
                vocablist._word2id[word] = word_index
                vocablist._word2cn[word] = cn
                vocablist._word2class[word] = class_index
                vocablist._class2size[class_index] += 1
                if class_index not in vocablist._class2range:
                    vocablist._class2range[class_index] = (word_index, word_index+1)
                else:
                    start, end = vocablist._class2range[class_index]
                    vocablist._class2range[class_index] = (start, word_index+1)
                return 0

        vocablist = _TinyCRnnLMVocabList()

        while True:
            flag = set_vocab(vocablist, fi)
            if flag == 1:
                break

        return vocablist

    def get_embed_id(self, word):
        return self._word2id[word]

    def get_class_id(self, word):
        return self._word2class[word]

    def get_class_size(self, class_id):
        return self._class2size[class_id]

    def get_class_range(self, class_id):
        return self._class2range[class_id]


class TinyCRnnLM(SaveLoad):

    """ tiny wrapper for CRnnLM (RNNLM Toolkit http://rnnlm.org)
    this wrapper only supports forward propagation.
    """

    def __init__(self, vocab_size, hidden_size, class_size, vocablist):
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.class_size = class_size

        self._vocablist = vocablist

        self._U = numpy.zeros((hidden_size, vocab_size))
        self._W = numpy.zeros((hidden_size, hidden_size))
        self._V = numpy.zeros((vocab_size, hidden_size))
        self._C = numpy.zeros((class_size, hidden_size))

        self._neu0 = -1
        self._last_neu1 = 0.1 * numpy.ones((hidden_size, ))
        self._neu1 = numpy.zeros((hidden_size, ))
        self._neu2 = numpy.zeros((vocab_size,))
        self._neuc = numpy.zeros((class_size, ))

        self._independent = False

    @classmethod
    def read(cls, rnnlm_file):
        vocab_size = 0
        hidden_size = 0
        class_size = 0
        vocablist = None
        U, V = None, None
        independent = False

        with open(rnnlm_file) as fi:
            header = _read_header(fi)
            hidden_size = header["hidden layer size"]
            class_size = header["class size"]
            vocab_size = header["vocabulary size"]
            independent = header["independent sentences mode"] == 1
            vocablist = _TinyCRnnLMVocabList.read(fi)
            _ = _read_hidden_layer_activation(fi)
            U = _read_weight(fi)
            _ = _read_weight(fi)
            V = _read_weight(fi)
            _ = _read_direct_connections(fi)

        rnnlm = TinyCRnnLM(vocab_size, hidden_size, class_size, vocablist)

        U = U.reshape((hidden_size, vocab_size + hidden_size))
        V = V.reshape((vocab_size + class_size, hidden_size))

        rnnlm._U = numpy.copy(U[:, :vocab_size])
        rnnlm._W = numpy.copy(U[:, vocab_size:])
        rnnlm._V = numpy.copy(V[:vocab_size, :])
        rnnlm._C = numpy.copy(V[vocab_size:, :])

        rnnlm._independent = independent

        return rnnlm

    def fprop(self, word, next_word):
        """ forward propagation
        :param str word: current word
        :param str next_word: next word
        :return: conditional probability for next word (given current word)
        :rtype: float
        """
        self._neu0 = self._vocablist.get_embed_id(word)

        if self._neu0 != -1:
            self._neu1 = \
                numpy.dot(self._W, self._last_neu1) + self._U[:, self._neu0]
        else:
            self._neu1 = numpy.dot(self._W, self._last_neu1)
        self._neu1 = _sigmoid(self._neu1)

        self._neuc = numpy.dot(self._C, self._neu1)
        self._neuc = _softmax(self._neuc)

        i = self._vocablist.get_embed_id(next_word)
        c = self._vocablist.get_class_id(next_word)
        start, end = self._vocablist.get_class_range(c)

        if i != -1:
            neu = numpy.dot(self._V[start:end, :], self._neu1)
            self._neu2[start:end] = _softmax(neu)
            return self._neu2[i] * self._neuc[c], self._neu1
        else:
            # penalty probability
            return 1e-100, self._neu1

    def cache_context(self, neu1=None):
        if neu1 is None:
            neu1 = self._neu1
        self._last_neu1 = numpy.copy(neu1)

    def flush_context(self, force=False):
        if force or self._independent:
            self._last_neu1 = 0.1 * numpy.ones((self.hidden_size, ))


def perplexity(rnnlm, test_file, eos='</s>'):
    """ compute test-set perplexity
    :param TinyCRnnLM rnnlm: rnn lang-model
    :param str test_file: test-set file
    :param str eos: end of symbol
    :return: test-set perplexity
    :rtype: float
    """
    logp = 0.
    cn = 0
    with open(test_file, 'r') as fi:
        for line in fi:
            words = line.rstrip().split(' ')
            words.append(eos)
            word = eos
            for next_word in words:
                p, _ = rnnlm.fprop(word, next_word)
                if p != 1e-100:
                    logp += numpy.log(p)
                    cn += 1
                rnnlm.cache_context()
                word = next_word
            rnnlm.flush_context()
    return numpy.exp(- logp / cn)
