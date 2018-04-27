#!/usr/bin/env python3

import io
import os
import sys
import logging

import numpy as np
import tensorflow as tf

from typing import List

from daikon import vocab
from daikon import compgraph
from daikon import constants as C


def softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=0)

def load_vocabs(load_from: str):

    source_vocab = vocab.Vocabulary()
    source_vocab.load(os.path.join(load_from, C.SOURCE_VOCAB_FILENAME))
    target_vocab = vocab.Vocabulary()
    target_vocab.load(os.path.join(load_from, C.TARGET_VOCAB_FILENAME))

    return source_vocab, target_vocab

def translate_line(session,
                   line,
                   source_vocab,
                   target_vocab,
                   encoder_inputs,
                   decoder_inputs,
                   decoder_targets,
                   decoder_logits):
    """
    TODO
    """
    source_ids = np.array(source_vocab.get_ids(line.split())).reshape(1, -1)

    translated_ids = []

    for _ in range(C.TRANSLATION_MAX_LEN):

        # target ids will serve as decoder inputs and decoder targets,
        # but decoder targets will not be used to compute logits
        target_ids = np.array([C.BOS_ID] + translated_ids).reshape(1, -1)

        feed_dict = {encoder_inputs: source_ids,
                     decoder_inputs: target_ids,
                     decoder_targets: target_ids}
        logits_result = session.run([decoder_logits], feed_dict=feed_dict)

        # first session result, first item in batch, target symbol at last position
        next_symbol_logits = logits_result[0][0][-1]
        next_id = np.argmax(next_symbol_logits)

        if next_id in [C.EOS_ID, C.PAD_ID]:
            break

        translated_ids.append(next_id)

    words = target_vocab.get_words(translated_ids)

    return ' '.join(words)

def translate_lines(load_from: str, input_lines: List[str], train_mode: bool = False, **kwargs):
    """
    TODO
    """
    source_vocab, target_vocab = load_vocabs(load_from)

    # fix batch_size to 1
    encoder_inputs, decoder_targets, decoder_inputs, _, _, decoder_logits, _ = compgraph.define_computation_graph(source_vocab.size, target_vocab.size, 1)

    saver = tf.train.Saver()

    with tf.Session() as session:

        # load model
        saver.restore(session, os.path.join(load_from, C.MODEL_FILENAME))

        translations = []

        for line in input_file_handle:
            translation = translate_line(session, line, source_vocab, target_vocab, encoder_inputs, decoder_inputs, decoder_targets, decoder_logits)
            translations.append(translation)

    return translations


def translate_file(load_from: str, input_file_handle: io.TextIOWrapper, output_file_handle: io.TextIOWrapper, **kwargs):
    """
    TODO
    """
    source_vocab, target_vocab = load_vocabs(load_from)

    # fix batch_size to 1
    encoder_inputs, decoder_targets, decoder_inputs, _, _, decoder_logits, _ = compgraph.define_computation_graph(source_vocab.size, target_vocab.size, 1)

    saver = tf.train.Saver()

    with tf.Session() as session:

        # load model
        saver.restore(session, os.path.join(load_from, C.MODEL_FILENAME))

        for line in input_file_handle:
            translation = translate_line(session, line, source_vocab, target_vocab, encoder_inputs, decoder_inputs, decoder_targets, decoder_logits)
            output_file_handle.write(translation + "\n")
