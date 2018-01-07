#!/usr/b:in/env python
# -*- coding: utf-8 -*-

# Find synset (from several variants) for the sentence.
# For each sentence in the input file sentences.py

from __future__ import division # https://stackoverflow.com/a/21317109/1173350
import logging
import os
import codecs
import operator
import collections
import numpy as np

# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from data.sentences_in import sentences
from data.synsets import synsets

sys.path.append(os.path.abspath('../')) # add parent folder, access to 'lib'
import lib.string_util

from gensim.models import Word2Vec, keyedvectors

sys.path.append(os.path.abspath('../')) # add parent folder, access to 'lib'
import lib.filter_vocab_words
import lib.string_util
import lib.synset

import lib.internal_set
import test_synset_for_sentence.lib_sfors.synset_selector

import configus
model = keyedvectors.KeyedVectors.load_word2vec_format(configus.MODEL_PATH, binary=True)

def diff(list1, list2):
    list2 = set(list2)
    return [item for item in list1 if item not in list2]

print "Word2vec model: {}\n".format(configus.MODEL_NAME)

print "__________________SYNSETS________________"
lib.filter_vocab_words.filterSynsets( synsets, model.vocab ) # filter synsets, remove words absented in RusVectores

#print "__________________SENTENCES________________"
for sent in sentences:
#    print "\n\nSentence:", sent, "has lemmas:"
    filtered_list = lib.filter_vocab_words.filterVocabWords( sentences[sent]["lemmas"], model.vocab )
#    print 'OLD LIST:', ', '.join(sentences[sent]['lemmas'])
#    print 'DELETED:', ', '.join(diff(sentences[sent]['lemmas'],filtered_list))
#    print 'NEW LIST:', ', '.join(filtered_list)
    sentences[sent]['lemmas'] = filtered_list

print "__________________EXPERIMENT 1________________"
alg1_sum_1 = 0 # number of positive answers (the same as answer of expert)
alg1_sum_0 = 0 # number of negative answers
for sent in sentences:
    # the list 'sentences' will be updated in the function below
    (a, b) = test_synset_for_sentence.lib_sfors.synset_selector.selectSynsetForSentenceByAverageSimilarity (
                                                                sent, sentences, synsets, model )
    alg1_sum_1 += a
    alg1_sum_0 += b
print "Right answers:", str(alg1_sum_1)+',', "wrong answers:", str(alg1_sum_0)


epsFile = open('data/epsilon_out.csv','w')
epsFile.write(u"Epsilon\tRight\tWrong\n")

print "__________________EXPERIMENT 2________________"
# eps, near_set_num, far_set_num, alien_degree
#for eps in range(0.05,0.95,0.05):
for eps in np.arange(0.0, 1.0, 0.01):
    alg2_expert_plus  = 0
    alg2_expert_minus = 0
    for sent in sentences:
        # the list 'sentences' will be updated in the function below
        (a, b) = test_synset_for_sentence.lib_sfors.synset_selector.selectSynsetForSentenceByAlienDegree (
                                                                        sent, sentences, synsets, model, eps )
        alg2_expert_plus  += a
        alg2_expert_minus += b
    
    print "Epsilon:", str(eps)+',', "right answers:", str(alg2_expert_plus)+',', "wrong answers:", str(alg2_expert_minus)

    epsFile.write(u"{}\t{}\t{}\n".format(str(eps), str(alg2_expert_plus), str(alg2_expert_minus)))
epsFile.close()
sys.exit("\nLet's stop and think.")

sentFile = open('data/sentence_out.csv','w')
sentFile.write(u"Sentence\tLemma\tN lemmas\tExpert\tAlg1(average)\tAlg2(alien)\tAlg1+\tAlg2+\n")

for sent in sentences:
#    sentFile.write(sent + "\t" + str(sentences[sent]['synset_exp']) + "\t" + str(sentences[sent]['synset_alg1']) + "\t" + str(sentences[sent]['synset_alg2']) + "\n")
    sentFile.write(u"{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n"
            .format(sent,sentences[sent]['lemma'],
                         str(len(sentences[sent]['lemmas'])),
                         str(sentences[sent]['synset_exp']),
                         str(sentences[sent]['synset_alg1']),
                         str(sentences[sent]['synset_alg2']),
                         str(sentences[sent]['alg1_right']),
                         str(sentences[sent]['alg2_right'])))
sentFile.close()

sys.exit("\nLet's stop and think.")


line1 = [u'гам', u'гвалт', u'грохот', u'гул', u'устройство', u'странность']
#line1 = u"гам гвалт грохот гул" # without "шум "
line2 = [u'помеха', u'возмущение', u'роза', u'табуретка', u'мышь']
#ine2 = u"помеха возмущение"    # without "шум "

#gr1   = line1.split()
#gr2   = line2.split()

words1 = lib.filter_vocab_words.filterVocabWords( line1, model.vocab )
print lib.string_util.joinUtf8( ",", words1 )                                # after filter, now there are only words with vectors

#arr_vectors1 = []
#for w in words1:
#    # print u"    - '{}'".format( model[ w ] )
#    arr_vectors1.append( model[ w ] )

words2 = lib.filter_vocab_words.filterVocabWords( line2, model.vocab )
print lib.string_util.joinUtf8( ",", words2 )                                # after filter, now there are only words with vectors

#arr_vectors2 = []
#for w in words2:
#    # print u"    - '{}'".format( model[ w ] )
#    arr_vectors2.append( model[ w ] )

d = model.n_similarity(words1, words2)
print u"d = {}".format( d )

sys.exit("\nLet's stop and think.")

print u"d = {} | gr1={} | gr2={}".format( d, test_word,  lib.string_util.joinUtf8( ",", gr1 ), 
                                                         lib.string_util.joinUtf8( ",", gr2 ) )

# sys.exit("\nLet's stop and think.")
