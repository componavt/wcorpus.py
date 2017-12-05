#!/usr/b:in/env python
# -*- coding: utf-8 -*-

# Find synset (from several variants) for the sentence.
# For each sentence in the input file sentences.py

import logging
import sys
import os
import codecs
import operator
import collections



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

import configus
model = keyedvectors.KeyedVectors.load_word2vec_format(configus.MODEL_PATH, binary=True)

def diff(list1, list2):
    list2 = set(list2)
    return [item for item in list1 if item not in list2]

print "Word2vec model: {}\n".format(configus.MODEL_NAME)

print "Deleted synsets"

print "__________________SYNSETS________________"
for lemma in synsets:
    for synset_id in synsets[lemma]:
        filtered_list = lib.filter_vocab_words.filterVocabWords( synsets[lemma][synset_id], model.vocab )
        if len(filtered_list) < 2:
            print u"\n{}".format( lemma )
        # print u'\n', lemma
            print 'OLD LIST:', ', '.join(synsets[lemma][synset_id])
            print 'DELETED:', ', '.join(diff(synsets[lemma][synset_id],filtered_list))
            print 'NEW SYNSET:', ', '.join(filtered_list)
        synsets[lemma][synset_id] = filtered_list

#print "__________________SENTENCES________________"
for sent in sentences:
#    print "\n\nSentence:", sent, "has lemmas:"
    filtered_list = lib.filter_vocab_words.filterVocabWords( sentences[sent]["lemmas"], model.vocab )
#    print 'OLD LIST:', ', '.join(sentences[sent]['lemmas'])
#    print 'DELETED:', ', '.join(diff(sentences[sent]['lemmas'],filtered_list))
#    print 'NEW LIST:', ', '.join(filtered_list)
    sentences[sent]['lemmas'] = filtered_list

print "__________________EXPERIMENT________________"
for sent in sentences:
    print "\n\nSENTENCE:", sent
    lemma = sentences[sent]['lemma']
    if len(sentences[sent]['lemmas'])> 0 :
        max_d = 0
        max_i = 0
        print "LEMMA LIST:", ', '.join(sentences[sent]['lemmas'])
        print "EXPERT ANSWER:", ', '.join(synsets[lemma][sentences[sent]['synset_exp']])
        for synset_id in synsets[lemma]:
            if len(synsets[lemma][synset_id]) > 0 :
                d = abs(model.n_similarity(sentences[sent]['lemmas'], synsets[lemma][synset_id]))
                print d, ':', ', '.join(synsets[lemma][synset_id])
                if d > max_d:
                    max_d = d
                    max_i = synset_id
            else :
                print synset_id, 'synset is empty'

        if (max_i == 0):
            sentences[sent]['synset_alg1'] = '-'
            print '-'
        else:
            sentences[sent]['synset_alg1'] = max_i
            if sentences[sent]['synset_exp'] == max_i:
                print 1
            else: 
                print 0

    else:
        print 'Lemma list empty'

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
