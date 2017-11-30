#!/usr/bin/env python
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

for lemma in synsets:
	for synset_id in synsets[lemma]:
		filtered_list = lib.filter_vocab_words.filterVocabWords( synsets[lemma][synset_id], model.vocab )
		print '\n', lemma
		print 'Deleted:', ', '.join(diff(synsets[lemma][synset_id],filtered_list))
		print 'New synset:', ', '.join(filtered_list)
		synsets[lemma][synset_id] = filtered_list


for sent in sentences:
#    print u"Sentence: {} has lemmas: ".format( sent ) 
#    print "Sentence: " + sent + " has lemmas: "
    print "\n\nSentence:", sent, "has lemmas:"
#    print sentences[sent]['lemmas']
    for lemma in sentences[sent]["lemmas"]:
#        print u"{}".format( lemma ),
		print lemma,


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
