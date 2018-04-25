#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Authors:
# Samuel Läubli <laeubli@cl.uzh.ch>
# Mathias Müller <mmueller@cl.uzh.ch>

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

PAD_ID = 0
EOS_ID = 1
BOS_ID = EOS_ID
UNK_ID = 2

PAD = '<pad>'
EOS = '<eos>'
BOS = EOS
UNK = '<unk>'

MODEL_FILENAME = 'model'
SOURCE_VOCAB_FILENAME = 'vocab.source.json'
TARGET_VOCAB_FILENAME = 'vocab.target.json'

# max number of tokens per sequence
MAX_LEN = 50
SOURCE_VOCAB_SIZE = 1000
TARGET_VOCAB_SIZE = 1000

EMBEDDING_SIZE = 128
# size of LSTM hidden state vectors
HIDDEN_SIZE = 512

NUM_LAYERS = 1
# truncate backpropagation though unrolled recurrent network
NUM_STEPS = MAX_LEN

LEARNING_RATE = 0.0001
